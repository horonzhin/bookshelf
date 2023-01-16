from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView, CreateView

from books.forms import AddBookForm
from books.models import Basket, Book, BookCategory
from common.views import TitleMixin


class BookListView(TitleMixin, ListView):
    model = Book
    template_name = 'books/books_list.html'
    # список книг полученных из базы будет доступен в шаблоне через переменную object_list, чтобы придать ему
    # более понятное название, нужно добавить атрибут context_object_name и дать ему более подходящее название.
    context_object_name = 'books_list'
    paginate_by = 8
    title = 'Bookshelf - Книжная полка'

    # метод для фильтрации по категориям
    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = BookCategory.objects.all()
        return context


class AuthorBooksListView(TitleMixin, ListView):
    model = Book
    template_name = 'books/author-books_list.html'
    context_object_name = 'author_books_list'
    paginate_by = 8
    title = 'Bookshelf - Книги автора'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # сортирую авторов по id (я первый)
        context['author_books'] = Book.objects.all().filter(author=1)
        return context


# Класс ниже отвечает за детальное отображение отдельных страниц книг на примере одного шаблона.
# Работает с одной записью из бд, а не со всем списком, как ListView. Название файла шаблона должно соответсвовать
# следующему "название модели(в нижнем регистре)_detail.html"
class BookDetailView(DetailView):
    model = Book
    template_name = 'books/book_detail.html'
    context_object_name = 'book_detail'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # сортирую авторов по id (я первый)
        context['author_books'] = Book.objects.all().filter(author=1)
        return context


class AddBookView(TitleMixin, CreateView):
    model = Book
    form_class = AddBookForm
    template_name = 'books/add_book.html'
    success_url = reverse_lazy('books')
    title = 'Bookshelf - Добавление книги'

    # def form_valid(self, form):
    #     form.save()
    #     return HttpResponseRedirect('/')

    # Вариант решения со stackoverflow:
    # https://stackoverflow.com/questions/8996451/save-new-foreign-key-with-django-form
    # https://stackoverflow.com/questions/9010852/catching-validation-errors-in-django-forms

    # def testone(request):
    #     if request.method == 'POST':  # If the form has been submitted...
    #         form = FilmForm(request.POST)  # A form bound to the POST data
    #
    #         if form.is_valid():  # All validation rules pass
    #             if form.cleaned_data['new_studio']:
    #                 studio, created = Studio.objects.get_or_create(name=form.cleaned_data['new_studio'])
    #                 new_film = form.save(commit=False)
    #                 new_film.studio = studio
    #             else:
    #                 new_film = form
    #
    #             new_film.save()
    #             return HttpResponseRedirect('/')  # Redirect after POST
    #         else:
    #             form = FilmForm()  # An unbound form
    #
    #         return render_to_response('testone.html', {
    #             'form': form
    #         }, context_instance=RequestContext(request))

    # todo = не сохраняет в базу книгу и перенаправляет на страницу books/author-books/1/?


# декоратор доступа, чтобы представление не срабатывало если user не авторизован
@login_required
def basket_add(request, book_id):
    book = Book.objects.get(id=book_id)
    # возьмем все корзины user с определенной книгой.
    baskets = Basket.objects.filter(user=request.user, book=book)

    # Если корзины нет, то она создатся, если есть, то увеличется кол-во на 1
    if not baskets.exists():
        Basket.objects.create(user=request.user, book=book, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()

    # после вернем user туда где он был
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


class IndexView(TitleMixin, TemplateView):
    template_name = 'books/index.html'
    title = 'Bookshelf'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # показываем последние три добавленные книги
        context['books'] = Book.objects.filter(user=self.request.user.id).order_by('-id')[:3]
        # показываем последние две добавленные книги в избранное (id избранного = 1)
        context['favourite'] = Book.objects.filter(user=self.request.user.id).order_by('category_id')[:2]
        return context


class About(TitleMixin, TemplateView):
    template_name = 'books/about.html'
    title = 'Bookshelf - Об авторе'


class Contacts(TitleMixin, TemplateView):
    template_name = 'books/contacts.html'
    title = 'Bookshelf - Контакты'
