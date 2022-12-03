from django.contrib.auth.decorators import login_required
from django.urls import path

from orders import views

app_name = 'orders'

urlpatterns = [
    path('order-create/', views.OrderCreateView.as_view(), name='order_create'),
]