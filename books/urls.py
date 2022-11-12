from django.urls import path
from books import views

app_name = 'books'

urlpatterns = [
    path('', views.BooksList.as_view(), name='books_list'),
    # path('books/', views.BookListView.as_view(), name='books_list'),
    path('author-books/', views.AuthorBooksList.as_view(), name='author-books_list'),
    path('baskets/add/<int:book_id>/', views.basket_add, name='basket_add'),
    path('baskets/remove/<int:basket_id>/', views.basket_remove, name='basket_remove'),
    path('book/', views.BookDetail.as_view(), name='book'),
    # path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
]