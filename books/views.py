from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect
from django.views import View
from django.views.generic import TemplateView
from books.models import Book, Basket
from users.models import User


class BooksList(TemplateView):
    template_name = 'books/books_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        books = Book.objects.all()
        context['books'] = books
        return context


class AuthorBooksList(TemplateView):
    template_name = 'books/author-books_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        books = Book.objects.all()
        context['books'] = books
        return context


# чтобы отобразить список данных из базы данных используем класс ListView. Класс ниже отвечает за отображение списка
# книг на странице с перечнем книг
# class BookListView(ListView):
#     model = Book
#     # указать путь к шаблону
#     template_name = 'books/books_list.html'
#     # список книг полученных из базы будет доступен в шаблоне через переменную object_list, чтобы придать ему
#     # более понятное название, нужно добавить атрибут context_object_name и дать ему более подходящее название.
#     context_object_name = 'books_list'


class BookDetail(TemplateView):
    template_name = 'books/book_detail.html'


# Класс ниже отвечает за детальное отображение отдельных страниц книг на примере одного шаблона.
# Работает с одной записью из бд, а не со всем списком, как ListView. Название файла шаблона должно соответсвовать
# следующему "название модели(в нижнем регистре)_detail.html"
# class BookDetailView(DetailView):
#     model = Book
#     template_name = 'books/book_detail.html'
#     context_object_name = 'book'

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


def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


class Index(TemplateView):
    template_name = 'books/index.html'


class About(TemplateView):
    template_name = 'books/about.html'


class Contacts(TemplateView):
    template_name = 'books/contacts.html'
