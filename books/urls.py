from django.urls import path
from books import views

app_name = 'books'

urlpatterns = [
    path('', views.BookListView.as_view(), name='books_list'),
    path('category/<int:category_id>', views.BookListView.as_view(), name='category'),
    path('page/<int:page>/', views.BookListView.as_view(), name='paginator'),
    path('author-books/', views.AuthorBooksListView.as_view(), name='author-books_list'),
    path('author-books/page/<int:page>/', views.AuthorBooksListView.as_view(), name='paginator-author'),
    path('book/', views.BookDetail.as_view(), name='book'),
    # path('/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('baskets/add/<int:book_id>/', views.basket_add, name='basket_add'),
    path('baskets/remove/<int:basket_id>/', views.basket_remove, name='basket_remove'),
]