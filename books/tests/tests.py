# -*- coding: utf-8 -*-

import bookshelf.wsgi
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from books.models import Book, BookCategory


class BookListViewTestCase(TestCase):
    """Reader's Bookshelf Page Test"""
    fixtures = ['books.json', 'author.json', 'category.json', 'cycle.json',
                'genre.json', 'series.json', 'user.json']

    def setUp(self):
        self.books = Book.objects.all()

    def test_list(self):
        """Test of show a list of books with pagination + common tests"""
        path = reverse('books:books_list')
        response = self.client.get(path)

        self._common_tests(response)
        self.assertEqual(list(response.context_data['books_list']), list(self.books[:8]))

    def test_list_with_category(self):
        """Test of show a list of books sorted by category + common tests"""
        category = BookCategory.objects.first()
        path = reverse('books:category', kwargs={'category_id': category.id})
        response = self.client.get(path)

        self._common_tests(response)
        self.assertEqual(
            list(response.context_data['books_list']),
            list(self.books.filter(category_id=category.id))
        )

    def _common_tests(self, response):
        """
        1. Checking page loading.
        2. Context loading check (title).
        3. Checking the correct template.
        """
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Bookshelf - Your bookshelf')
        self.assertTemplateUsed(response, 'books/books_list.html')


class AuthorBookListViewTestCase(TestCase):
    """Test of show the author's book list page"""
    fixtures = ['books.json', 'author.json', 'category.json', 'cycle.json',
                'genre.json', 'series.json', 'user.json']

    def setUp(self):
        self.books = Book.objects.all()
        self.path = reverse('books:author-books_list')
        self.response = self.client.get(self.path)

    def test_list(self):
        """
        1. Test of show a list of books with pagination
        2. Test for show a list of books sorted by author
        3. Common tests
        """
        self._common_tests(self.response)
        self.assertEqual(list(self.response.context_data['author_books_list']), list(self.books[:8]))
        self.assertEqual(
            list(self.response.context_data['author_books']),
            list(self.books.filter(author=1))
        )

    def _common_tests(self, response):
        """
        1. Checking page loading.
        2. Context loading check (title).
        3. Checking the correct template.
        """
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], "Bookshelf - Author's books")
        self.assertTemplateUsed(response, 'books/author-books_list.html')


class IndexViewTestCase(TestCase):
    """Home Page Test"""

    def test_view(self):
        """
        1. Checking page loading.
        2. Context loading check (title).
        3. Checking the correct template.
        """
        path = reverse('index')
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Bookshelf')
        self.assertTemplateUsed(response, 'books/index.html')


class AboutViewTestCase(TestCase):
    """Test pages About the Author"""

    def test_view(self):
        """
        1. Checking page loading.
        2. Context loading check (title).
        3. Checking the correct template.
        """
        path = reverse('about')
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Bookshelf - About the author')
        self.assertTemplateUsed(response, 'books/about.html')


class ContactsViewTestCase(TestCase):
    """Test pages with contacts"""

    def test_view(self):
        """
        1. Checking page loading.
        2. Context loading check (title).
        3. Checking the correct template.
        """
        path = reverse('contacts')
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Bookshelf - Contacts')
        self.assertTemplateUsed(response, 'books/contacts.html')
