from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView


def main_page(request, *args, **kwargs):
    return render(request, 'main/main_page.html', {})


class About(TemplateView):
    template_name = 'main/about.html'


class Contacts(TemplateView):
    template_name = 'main/contacts.html'
