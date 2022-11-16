from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect
from django.views import View
from django.views.generic import TemplateView, ListView
from books.models import Book, Basket, BookCategory
from users.models import User


class BookListView(ListView):
    model = Book
    template_name = 'books/books_list.html'
    # список книг полученных из базы будет доступен в шаблоне через переменную object_list, чтобы придать ему
    # более понятное название, нужно добавить атрибут context_object_name и дать ему более подходящее название.
    context_object_name = 'books_list'
    paginate_by = 4

    # метод для фильтрации по категориям
    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Книжная полка'
        context['categories'] = BookCategory.objects.all()
        return context


class AuthorBooksListView(ListView):
    model = Book
    template_name = 'books/author-books_list.html'
    context_object_name = 'author_books_list'
    paginate_by = 4

    # метод для фильтрации по категориям
    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Книги автора'
        context['categories'] = BookCategory.objects.all()
        return context


class BookDetail(TemplateView):
    template_name = 'books/book_detail.html'


# Класс ниже отвечает за детальное отображение отдельных страниц книг на примере одного шаблона.
# Работает с одной записью из бд, а не со всем списком, как ListView. Название файла шаблона должно соответсвовать
# следующему "название модели(в нижнем регистре)_detail.html"
# class BookDetailView(DetailView):
#     model = Book
#     template_name = 'books/book_detail.html'
#     context_object_name = 'book'


# декоратор доступа, чтобы представление не срабатывало если user не авторизован
@login_required
def basket_add(request, book_id):
    book = Book.objects.get(id=book_id)
    # возьмем все корзины user с определенной книгой.
    baskets = Basket.objects.filter(user=request.user, book=book)

    # Если корзины нет, то она создатся, если есть, то увеличется кол-во на 1
    if not baskets.exists():
        Basket.objects.create(user=request.user, book=book, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()

    # после вернем user туда где он был
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


class IndexView(TemplateView):
    template_name = 'books/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Bookshelf'
        # показываем последние три добавленные книги
        context['books'] = Book.objects.all().order_by('-id')[:3]
        # показываем последние две добавленные книги в избранное (id избранного = 1)
        context['favourite'] = Book.objects.all().order_by('category_id')[:2]
        return context


class About(TemplateView):
    template_name = 'books/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Об авторе'
        return context


class Contacts(TemplateView):
    template_name = 'books/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Контакты'
        return context
