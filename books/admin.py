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
    list_display = ['title', 'get_author', 'get_genre', 'cycle', 'series',
                    'status', 'isbn', 'published', 'price', 'user']
    list_filter = ['status']
    search_fields = ['title', 'isbn']
    # todo = добавить возможность поиска по полю с типом ManyToMany
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

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()


class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('book', 'quantity', 'created_timestamp')
    readonly_fields = ('created_timestamp',)
    extra = 0
