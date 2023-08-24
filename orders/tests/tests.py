# -*- coding: utf-8 -*-

from http import HTTPStatus
from django.test import TestCase
from django.urls import reverse

from users.models import User
from orders.models import Order


class SuccessTemplateViewTest(TestCase):
    """Test a page with a successful order"""

    def test_success_template_view(self):
        """
        1. Checking page loading.
        2. Context loading check (title).
        3. Checking the correct template.
        """
        path = reverse('orders:order_success')
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Bookshelf - Thank you for the order!')
        self.assertTemplateUsed(response, 'orders/success.html')


class CancelledTemplateViewTest(TestCase):
    """Test a page with a cancelled order"""

    def test_cancelled_template_view(self):
        """
        1. Checking page loading.
        2. Context loading check (title).
        3. Checking the correct template.
        """
        path = reverse('orders:order_canceled')
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Bookshelf - Checkout canceled')
        self.assertTemplateUsed(response, 'orders/canceled.html')


class OrderListViewTest(TestCase):
    """Test a page with a list of all orders"""

    def setUp(self):
        self.data = {'username': 'username', 'password': '1234567qQ'}
        self.path = reverse('orders:orders_list')
        self.user = User.objects.create_user(**self.data)
        self.order = Order.objects.create(initiator=self.user)
        self.client.force_login(self.user)

    def test_order_list_view(self):
        """
        1. Checking page loading.
        2. Context loading check (title).
        3. Checking the correct template.
        """
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Bookshelf - Orders')
        self.assertTemplateUsed(response, 'orders/orders.html')


class OrderDetailViewTest(TestCase):
    """Test a page with a detailed order display"""

    def setUp(self):
        self.data = {'username': 'username', 'password': '1234567qQ'}
        self.user = User.objects.create_user(**self.data)
        self.order = Order.objects.create(initiator=self.user)

    def test_order_detail_view(self):
        """
        1. Checking page loading.
        2. Context loading check (title).
        3. Checking the correct template.
        """
        response = self.client.get(reverse('orders:order_detail', args=[self.order.id]))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'orders/order_detail.html')
        self.assertEqual(response.context_data['title'], 'Bookshelf - Order #' + str(self.order.id))


class OrderCreateViewTest(TestCase):
    # todo: тест для OrderCreateView
    pass
