# -*- coding: utf-8 -*-

import bookshelf.wsgi
from datetime import timedelta
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now

from users.models import EmailVerification, User


class UserRegistrationViewTest(TestCase):

    def setUp(self):
        self.data = {
            'first_name': 'First', 'last_name': 'Last', 'username': 'username',
            'email': 'email@mail.ru', 'password1': '1234567qQ', 'password2': '1234567qQ'
        }
        self.path = reverse('users:register')

    def test_user_registration_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Bookshelf - Регистрация')
        self.assertEqual(response.template_name[0], 'users/register.html')

    def test_user_registration_post_success(self):
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
        User.objects.create(username=self.data['username'])
        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Пользователь с таким именем уже существует.', html=True)
