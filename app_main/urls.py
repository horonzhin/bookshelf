from django.urls import path
from .import views

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('contacts/', views.Contacts.as_view(), name='contacts'),
    path('about/', views.About.as_view(), name='about')
]