from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView


class Index(TemplateView):
    template_name = 'books/index.html'


class BooksList(TemplateView):
    template_name = 'books/books_list.html'


class Book(TemplateView):
    template_name = 'books/book.html'


class About(TemplateView):
    template_name = 'books/about.html'


class Contacts(TemplateView):
    template_name = 'books/contacts.html'
