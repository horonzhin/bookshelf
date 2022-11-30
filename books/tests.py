# -*- coding: utf-8 -*-

import bookshelf.wsgi
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from books.models import Book, BookCategory


class BookListViewTestCase(TestCase):
    fixtures = ['books.json', 'author.json', 'category.json', 'cycle.json',
                'genre.json', 'series.json', 'status.json', 'user.json']

    def setUp(self):
        self.books = Book.objects.all()

    def test_list(self):
        path = reverse('books:books_list')
        response = self.client.get(path)

        self._common_tests(response)
        self.assertEqual(list(response.context_data['books_list']), list(self.books[:8]))

    def test_list_with_category(self):
        category = BookCategory.objects.first()
        path = reverse('books:category', kwargs={'category_id': category.id})
        response = self.client.get(path)

        self._common_tests(response)
        self.assertEqual(
            list(response.context_data['books_list']),
            list(self.books.filter(category_id=category.id))
        )

    def _common_tests(self, response):
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Bookshelf - Книжная полка')
        self.assertEqual(response.template_name[0], 'books/books_list.html')
        # self.assertTemplateUsed(response, 'books/books_list.html')


class AuthorBookListViewTestCase(TestCase):
    fixtures = ['books.json', 'author.json', 'category.json', 'cycle.json',
                'genre.json', 'series.json', 'status.json', 'user.json']

    def setUp(self):
        self.books = Book.objects.all()
        self.path = reverse('books:author-books_list')
        self.response = self.client.get(self.path)

    def test_list(self):
        self._common_tests(self.response)
        self.assertEqual(list(self.response.context_data['author_books_list']), list(self.books[:8]))
        self.assertEqual(
            list(self.response.context_data['author_books']),
            list(self.books.filter(author=1))
        )

    def _common_tests(self, response):
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Bookshelf - Книги автора')
        self.assertEqual(response.template_name[0], 'books/author-books_list.html')
        # self.assertTemplateUsed(response, 'books/author-books_list.html')


class IndexViewTestCase(TestCase):

    def test_view(self):
        path = reverse('index')
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Bookshelf')
        self.assertEqual(response.template_name[0], 'books/index.html')
        # self.assertTemplateUsed(response, 'books/index.html')


class AboutViewTestCase(TestCase):

    def test_view(self):
        path = reverse('about')
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Bookshelf - Об авторе')
        self.assertEqual(response.template_name[0], 'books/about.html')
        # self.assertTemplateUsed(response, 'books/about.html')


class ContactsViewTestCase(TestCase):

    def test_view(self):
        path = reverse('contacts')
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Bookshelf - Контакты')
        self.assertEqual(response.template_name[0], 'books/contacts.html')
        # self.assertTemplateUsed(response, 'books/contacts.html')
