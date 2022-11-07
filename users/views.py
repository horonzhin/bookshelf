from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse
from django.views import View
from users.models import User
from users.forms import UserLoginForm, UserRegistrationForm


class Login(View):

    def get(self, request):
        form = UserLoginForm()
        return render(request, 'users/login.html', context={'form': form})

    def post(self, request):
        form = UserLoginForm(data=request.POST)

        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)

            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))


# вариант представления через функцию
# def login(request):
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             username = request.POST['username']
#             password = request.POST['password']
#             user = auth.authenticate(username=username, password=password)
#             if user:
#                 auth.login(request, user)
#                 return HttpResponseRedirect(reverse('index'))
#     else:
#         form = UserLoginForm()
#     context = {'form': form}
#     return render(request, 'users/login.html', context)


class Registration(View):

    def get(self, request):
        form = UserRegistrationForm()
        return render(request, 'users/register.html', context={'form': form})

    def post(self, request):
        form = UserRegistrationForm(data=request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:login'))

