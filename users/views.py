from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from common.views import TitleMixin
from users.forms import UserLoginForm, UserProfileForm, UserRegistrationForm
from users.models import EmailVerification, User


class UserLoginView(TitleMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'Авторизация'


class UserRegistrationView(TitleMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    success_message = 'Поздравляю! Вы успешно зарегистрировались.'
    title = 'Регистрация'


class UserProfileView(TitleMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    title = 'Личный кабинет'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))


class EmailVerificationView(TitleMixin, TemplateView):
    title = 'Подтверждение электронной почты'
    template_name = 'users/email_verification.html'

    # сверяем полученный code с тем что в бд
    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        # не берем get(), т.к. если данного объекта не будет выскочит ошибка в шаблоне.
        # Используем filter, если объекта не будет вернется пустой список без ошибок
        email_verifications = EmailVerification.objects.filter(user=user, code=code)
        if email_verifications.exists() and not email_verifications.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('index'))


# декоратор доступа, чтобы представление не срабатывало если user не авторизован
# @method_decorator(login_required, name='dispatch')
# class Profile(View):
#
#     def get(self, request):
#         # для передачи данных в профиль заполняем instance
#         form = UserProfileForm(instance=request.user)
#         context = {
#             'title': '- Профиль',
#             'form': form,
#             # покажем user только те книги которые он добавил себе.
#             # Если указать objects.all() будут все книги всех user
#             'baskets': Basket.objects.filter(user=request.user),
#         }
#         return render(request, 'users/profile.html', context)
#
#     def post(self, request):
#         # чтобы перезаписать, а не создать новый добавляем instance=request.user
#         # а для загрузки картинок добавить files=request.FILES
#         # (не забыть в шаблоне в тэг <form> добавить enctype="multipart/form-data)"
#         form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
#
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('users:profile'))
#         else:
#             print(form.errors)


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


# class Registration(View):
#     title = '- Регистрация'
#
#     def get(self, request):
#         form = UserRegistrationForm()
#         return render(request, 'users/register.html', context={'form': form, 'title': self.title})
#
#     def post(self, request):
#         form = UserRegistrationForm(data=request.POST)
#
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Поздравляю! Вы успешно зарегистрировались.')
#             return HttpResponseRedirect(reverse('users:login'))
#
#         return render(request, 'users/register.html', context={'form': form, 'title': self.title})


# class Login(TitleMixin, View):
#     title = 'Авторизация'
#
#     def get(self, request):
#         form = UserLoginForm()
#         return render(request, 'users/login.html', context={'form': form})
#
#     def post(self, request):
#         form = UserLoginForm(data=request.POST)
#
#         if form.is_valid():
#             username = request.POST['username']
#             password = request.POST['password']
#             user = auth.authenticate(username=username, password=password)
#
#             if user:
#                 auth.login(request, user)
#                 return HttpResponseRedirect(reverse('index'))
#
#         return render(request, 'users/login.html', context={'form': form, 'title': self.title})


# def logout(request):
#     auth.logout(request)
#     return HttpResponseRedirect(reverse('index'))
