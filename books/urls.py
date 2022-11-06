from django.urls import path
from books import views

app_name = 'books'

urlpatterns = [
    path('', views.BooksList.as_view(), name='books_list'),
    # path('books/', views.BookListView.as_view(), name='books_list'),
    path('book/', views.BookDetail.as_view(), name='book'),
    # path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
]