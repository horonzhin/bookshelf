from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, TemplateView

from books.forms import AddBookForm
from books.models import Basket, Book, BookCategory
from common.views import TitleMixin


class BookListView(TitleMixin, ListView):
    """View of the reader's book list"""
    model = Book
    template_name = 'books/books_list.html'
    context_object_name = 'books_list'  # for a clear reference in the template, because by default -> object_list
    paginate_by = 8
    title = 'Bookshelf - Your bookshelf'

    def get_queryset(self):
        """Filtering books by category, if the category is not selected, we show everything"""
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        """Give the books filtered by category to the template"""
        context = super().get_context_data(**kwargs)
        context['categories'] = BookCategory.objects.all()
        return context


class AuthorBooksListView(TitleMixin, ListView):
    """View of the author's book list"""
    model = Book
    template_name = 'books/author-books_list.html'
    context_object_name = 'author_books_list'
    paginate_by = 8
    title = "Bookshelf - Author's books"

    def get_context_data(self, *, object_list=None, **kwargs):
        """Author's book filter (author id = 1)"""
        context = super().get_context_data(**kwargs)
        context['author_books'] = Book.objects.all().filter(author=1)
        return context


class BookDetailView(DetailView):
    """Detailed view of information about the book"""
    model = Book
    template_name = 'books/book_detail.html'
    context_object_name = 'book_detail'

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        1. Detailed viewing of the author's books (author_id = 1) contains other data
        2. Show the title of the book
        """
        context = super().get_context_data(**kwargs)
        context['author_books'] = Book.objects.all().filter(author=1)
        context['title'] = f'Bookshelf - {self.object.title}'
        return context


class AddBookView(TitleMixin, CreateView):
    """View of adding a new book"""
    model = Book
    form_class = AddBookForm
    template_name = 'books/add_book.html'
    success_url = reverse_lazy('books:books_list')
    title = 'Bookshelf - Adding a book'

    def form_valid(self, form):
        # add the user to the "instance" because the field is required.
        form.instance.user = self.request.user
        return super().form_valid(form)


@login_required  # the view will not work if the user is not logged in
def basket_add(request, book_id):
    """Adding books to the basket"""
    Basket.create_or_update(book_id, request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])  # return the user to where he was


@login_required
def basket_remove(request, basket_id):
    """Delete basket"""
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


class IndexView(TitleMixin, TemplateView):
    """Home Page View"""
    template_name = 'books/index.html'
    title = 'Bookshelf'

    def get_context_data(self, **kwargs):
        """
        1. Show last three added books
        2. Show the last two books added to favorites
        """
        context = super().get_context_data(**kwargs)
        context['books'] = Book.objects.filter(user=self.request.user.id).order_by('-id')[:3]
        context['favourite'] = Book.objects.filter(user=self.request.user.id).order_by('category_id')[:2]
        return context


class About(TitleMixin, TemplateView):
    """View of the page about the author"""
    template_name = 'books/about.html'
    title = 'Bookshelf - About the author'


class Contacts(TitleMixin, TemplateView):
    """View of the contact page"""
    template_name = 'books/contacts.html'
    title = 'Bookshelf - Contacts'
