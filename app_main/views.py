from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView


def main_page(request, *args, **kwargs):
    return render(request, 'main/main_page.html', {})


class Contacts(TemplateView):
    template_name = 'main/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        email = 'horonzhin@gmail.com'
        phone = '+7 (921) 571-35-32'
        context['email'] = email
        context['phone'] = phone
        return context
