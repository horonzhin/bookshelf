from django.contrib import admin

from books.models import (Author, Basket, Book, BookCategory, Cycle, Genre,
                          Series)


@admin.register(BookCategory)
class Category(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'country', 'birthday', 'death']
    list_filter = ['country']
    search_fields = ['last_name']


@admin.register(Cycle)
class CycleAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'cycle', 'series', 'get_genre', 'get_author',
                    'status', 'isbn', 'published', 'price', 'user']
    list_filter = ['status']
    # author__first_name and author__last_name adds the ability to search by field MtM
    search_fields = ['title', 'isbn', 'author__first_name', 'author__last_name']
    readonly_fields = ['user']
    fieldsets = (
        ('Сведения о книги', {
            'fields': ('title', 'author', 'cover', 'isbn', 'published', 'genre',
                       'cycle', 'series', 'annotation', 'price', 'stripe_book_price_id', 'text')
        }),
        ('Блок читателя', {
            'fields': ('user', 'status', 'rating', 'category', 'first_reading', 'second_reading', 'third_reading')
        })
    )

    def get_author(self, object):
        """To display authors in the admin panel list_display"""
        return ",".join([str(p) for p in object.author.all()])

    get_author.short_description = 'Авторы'

    def get_genre(self, object):
        """To display genres in the admin panel list_display"""
        return ",".join([str(p) for p in object.genre.all()])

    get_genre.short_description = 'Жанры'

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()


class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('book', 'quantity', 'created_timestamp')
    readonly_fields = ('created_timestamp',)
    extra = 0
