from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse
from django.views import View
from users.models import User
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm


class Login(View):

    def get(self, request):
        form = UserLoginForm()
        title = 'Bookshelf - Авторизация'
        return render(request, 'users/login.html', context={'form': form, 'title': title})

    def post(self, request):
        form = UserLoginForm(data=request.POST)

        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)

            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))


class Registration(View):

    def get(self, request):
        form = UserRegistrationForm()
        title = 'Bookshelf - Регистрация'
        return render(request, 'users/register.html', context={'form': form, 'title': title})

    def post(self, request):
        form = UserRegistrationForm(data=request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:login'))


class Profile(View):

    def get(self, request):
        # для передачи данных в профиль заполняем instance
        form = UserProfileForm(instance=request.user)
        title = 'Bookshelf - Профиль'
        return render(request, 'users/profile.html', context={'form': form, 'title': title})

    def post(self, request):
        # чтобы перезаписать, а не создать новый добавляем instance=request.user
        # а для загрузки картинок добавить files=request.FILES
        # (не забыть в шаблоне в тэг <form> добавить enctype="multipart/form-data)"
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
        else:
            print(form.errors)


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
