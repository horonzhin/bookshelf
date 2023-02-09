# -*- coding: utf-8 -*-
from http import HTTPStatus

import stripe
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from books.models import Basket
from common.views import TitleMixin
from orders.forms import OrderForm
from orders.models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY


class SuccessTemplateView(TitleMixin, TemplateView):
    """View of a page with a successful order"""
    template_name = 'orders/success.html'
    title = 'Bookshelf - Thank you for the order!'


class CancelledTemplateView(TitleMixin, TemplateView):
    """View of a page with a cancelled order"""
    template_name = 'orders/canceled.html'
    title = 'Bookshelf - Checkout canceled'


class OrderListView(TitleMixin, ListView):
    """View of a page with a list of all orders"""
    template_name = 'orders/orders.html'
    title = 'Bookshelf - Orders'
    context_object_name = 'orders_list'
    ordering = '-created'  # sorting from new to old
    queryset = Order.objects.all()

    def get_queryset(self):
        """List of orders in which the user is the initiator (creator)"""
        queryset = super(OrderListView, self).get_queryset()
        return queryset.filter(initiator=self.request.user)


class OderDetailView(DetailView):
    """View of a page with a detailed order display"""
    template_name = 'orders/order_detail.html'
    model = Order

    def get_context_data(self, **kwargs):
        """Show the order number in the title"""
        context = super(OderDetailView, self).get_context_data(**kwargs)
        context['title'] = f'Bookshelf - Order #{self.object.id}'
        return context


class OrderCreateView(TitleMixin, CreateView):
    """Order creation page view"""
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:order_create')
    title = 'Bookshelf - Making an order'

    def post(self, request, *args, **kwargs):
        """Creating a page to which the user will be redirected when he clicks 'place an order'"""
        super(OrderCreateView, self).post(request, *args, **kwargs)
        baskets = Basket.objects.filter(user=self.request.user)
        checkout_session = stripe.checkout.Session.create(
            line_items=baskets.stripe_products(),  # data from the basket (product, price, quantity)
            # pass the ID to the metadata so that we can then run the logic in fulfill_order by the order ID
            metadata={'order_id': self.object.id},
            mode='payment',
            success_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_success')),  # red to the success page
            cancel_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_canceled')),  # red to the cancel page
        )
        return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)

    def form_valid(self, form):
        """Take the order initiator (creator) from the form and write it to the database for the order"""
        form.instance.initiator = self.request.user
        return super(OrderCreateView, self).form_valid(form)


@csrf_exempt
def stripe_webhook_view(request):
    """Event handler with a csrf token creation decorator"""
    payload = request.body  # got a response from stripe
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )  # take the stripe event from the response
    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    # if the event was completed successfully, then we will get the session and take the necessary data from there
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # Fulfill the purchase...
        fulfill_order(session)

    # Passed signature verification
    return HttpResponse(status=200)


def fulfill_order(session):
    """
    After the session is successfully created, we run the logic:
    1. Status change
    2. Saving purchase history
    3. Cleaning the trash
    """
    order_id = int(session.metadata.order_id)
    order = Order.objects.get(id=order_id)
    order.update_after_payment()
