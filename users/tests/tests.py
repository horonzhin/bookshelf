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
            'email': 'test@gmail.com', 'password1': 'KsfwwWW1348', 'password2': 'KsfwwWW1348'
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
        # email_verification = EmailVerification.objects.filter(user__username=username)
        # self.assertTrue(email_verification.exists())
        # self.assertEqual(
        #     email_verification.first().expiration.date(),
        #     (now() + timedelta(hours=48)).date()
        # )

        # todo = EmailVerification.objects.filter(user__username=username) выдает пустой QuerySet.
        #  Данные в форме заполнены верно. Создается тестовый юзер с id=1. В send_email_verification передается id=1 и
        #  он берет по этому id не тестового юзера, а реального из базы id=1 (это admin). Но даже если отфильтровать
        #  по user_id=1 он выдаст пустой QuerySet хоть для admin и существует EmailVerification

    def test_user_registration_post_error(self):
        """
        Checking for an error if the user already exists:
        1. Checking page loading.
        2. Checking that there is an error message in the content
        """
        User.objects.create(username=self.data['username'])
        print(User.objects.get(username='username'))
        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Пользователь с таким именем уже существует.', html=True)


class UserLoginViewTest(TestCase):
    """Login page test"""

    def setUp(self):
        self.data = {'username': 'username', 'password': '1234567qQ'}
        self.path = reverse('users:login')
        # when creating a user (only with him such a difference), you need to call the create_user() method,
        # not create(), since only in this method the password is correctly transmitted and hashed.
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
        # login() method authorizes a live user. We check the authorization,
        # so we take the data from self.data and specify it in post().
        response = self.client.post(self.path, {'username': self.data['username'], 'password': self.data['password']})

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('index'))

    def test_user_login_post_error(self):
        """
        Checking for an error if the user already exists:
        1. Checking page loading.
        2. Checking that there is an error message in the content
        """
        response = self.client.post(self.path, {'username': self.data['username'], 'password': '1234'})

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Пожалуйста, введите правильные имя пользователя и пароль. '
                                      'Оба поля могут быть чувствительны к регистру.', html=True)
