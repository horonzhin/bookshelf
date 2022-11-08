from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse
from django.views import View
from users.models import User
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm


class Login(View):
    title = 'Bookshelf - Авторизация'

    def get(self, request):
        form = UserLoginForm()
        return render(request, 'users/login.html', context={'form': form, 'title': self.title})

    def post(self, request):
        form = UserLoginForm(data=request.POST)

        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)

            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))

        return render(request, 'users/login.html', context={'form': form, 'title': self.title})


class Registration(View):
    title = 'Bookshelf - Регистрация'

    def get(self, request):
        form = UserRegistrationForm()
        return render(request, 'users/register.html', context={'form': form, 'title': self.title})

    def post(self, request):
        form = UserRegistrationForm(data=request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Поздравляю! Вы успешно зарегистрировались.')
            return HttpResponseRedirect(reverse('users:login'))

        return render(request, 'users/register.html', context={'form': form, 'title': self.title})


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


def logout(request):
    auth.logout(request)
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
