from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from books.models import Book


class Index(TemplateView):
    template_name = 'books/index.html'


class BooksList(TemplateView):
    template_name = 'books/books_list.html'

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


class About(TemplateView):
    template_name = 'books/about.html'


class Contacts(TemplateView):
    template_name = 'books/contacts.html'


# вариант представления через функцию
# def book(request, *args, **kwargs):
#     context = ['context']
#     return render(request, 'books/book.html', {'context': context})
