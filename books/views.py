from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView


def index(request, *args, **kwargs):
    return render(request, 'books/index.html', {})


class About(TemplateView):
    template_name = 'books/about.html'


class Contacts(TemplateView):
    template_name = 'books/contacts.html'
