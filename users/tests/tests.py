# -*- coding: utf-8 -*-

from datetime import timedelta
from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse
from django.utils.timezone import now

import bookshelf.wsgi
from users.models import EmailVerification, User


class UserRegistrationViewTest(TestCase):
    """Test of the registration page"""

    def setUp(self):
        self.data = {
            'first_name': 'First', 'last_name': 'Last', 'username': 'username',
            'email': 'email@mail.ru', 'password1': '1234567qQ', 'password2': '1234567qQ'
        }
        self.path = reverse('users:register')

    def test_user_registration_get(self):
        """
        1. Checking page loading.
        2. Context loading check (title).
        3. Checking the correct template.
        """
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Bookshelf - Registration')
        self.assertTemplateUsed(response, 'users/register.html')

    def test_user_registration_post_success(self):
        """
        1. Checking that the user is not yet in the database. After that, we pass the user's data to the response
        2. Checking for a redirect
        3. Checking for the correct redirect page
        4. Checking that a new user has been created in the database
        5. Checking that email verification was created in the database, which is linked to the user.
        6. Checking that the expiration date (without time) is correct
        """
        username = self.data['username']
        self.assertFalse(User.objects.filter(username=username).exists())
        response = self.client.post(self.path, self.data)

        # check creating of user
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:login'))
        self.assertTrue(User.objects.filter(username=username).exists())

        # check creating of email verification
        email_verification = EmailVerification.objects.filter(user__username=username)
        self.assertTrue(email_verification.exists())
        self.assertEqual(
            email_verification.first().expiration.date(),
            (now() + timedelta(hours=48)).date()
        )

        # todo = self.assertEqual(response.status_code, HTTPStatus.FOUND) - выдает 200 и не проходит
        # todo = self.assertRedirects(response, reverse('users:login')) - не проходит из-за проблемы выше
        # todo = User.objects.filter(username=username) и EmailVerification.objects.filter(user__username=username)
        #  выдает пустой QuerySet

    def test_user_registration_post_error(self):
        """
        Checking for an error if the user already exists:
        1. Checking page loading.
        2. Checking that there is an error message in the content
        """
        User.objects.create(username=self.data['username'])
        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Пользователь с таким именем уже существует.', html=True)


class UserLoginViewTest(TestCase):
    """Login page test"""

    def setUp(self):
        self.data = {'username': 'username', 'password': '1234567qQ'}
        self.path = reverse('users:login')
        # Здесь при создании юзера (только с ним такое отличие) нужно вызывать метод не create(),
        # а create_user(), так как только в этом методе правильно передается пароль и хешируется.
        # Можешь вовнутрь залезть в этот метод, чтобы посмотреть весь процесс)
        self.user = User.objects.create_user(**self.data)
        self.client = Client()

    def test_user_login_get(self):
        """
        1. Checking page loading.
        2. Context loading check (title).
        3. Checking the correct template.
        """
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Bookshelf - Authorization')
        self.assertTemplateUsed(response, 'users/login.html')

    def test_user_login_post_success(self):
        """
        Checking for authorization:
        1. Checking for a redirect upon successful authorization
        2. Checking for the correct redirect page
        """

        # Метод login() авторизует у тебя пользователя. Удобно, когда нужно в каких-то тестах
        # иметь авторизованного пользователя. Здесь же тест на авторизацию, поэтому тут точно вызов
        # login() не нужен. У тебя авторизация происходит в методе post(), когда данные юзера
        # отправляются во вьюху LoginView
        # self.client.login(username=self.user.username, password=self.user.password)

        # С теми данными, что ты авторизуешься в самой форме, то же самое и нужно отправлять в методе post().
        # И лучше брать сами данные из self.data, которые используются изначально для создания юзера.
        response = self.client.post(self.path, {'username': self.data['username'], 'password': self.data['password']})

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('index'))

        # todo = работает только с HTTPStatus.OK, но должен быть HTTPStatus.FOUND и редирект на главную

    def test_user_login_post_error(self):
        """
        Checking for an error if the user already exists:
        1. Checking page loading.
        2. Checking that there is an error message in the content
        """
        self.client.login(username=self.user.username, password='1234')
        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Пожалуйста, введите правильные имя пользователя и пароль. '
                                      'Оба поля могут быть чувствительны к регистру.', html=True)

        # todo = даже если указать, что пользователь логинится с правильными данными тест проходит
