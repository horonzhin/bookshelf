from django.urls import path

from api import views

app_name = 'api'

urlpatterns = [
    path('book-list/', views.BookListAPIView.as_view(), name='book_list'),
]