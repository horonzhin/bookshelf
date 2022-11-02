from django.contrib import admin
from books.models import Status, Genre, Author, Cycle, Series, Book


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Cycle)
class CycleAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'cycle', 'series', 'status', 'isbn', 'published']
    # todo = добавить возможность добавления в общий вид полей с типом ManyToMany
    list_filter = ['status']
    search_fields = ['title', 'isbn']
    # todo = добавить возможность поиска по полю с типом ManyToMany
    fieldsets = (
        ('Сведения о книги', {
            'fields': ('title', 'author', 'cover', 'isbn', 'published', 'genre', 'cycle', 'series', 'annotation')
        }),
        ('Блок читателя', {
            'fields': ('status', 'rating', 'first_reading', 'second_reading', 'third_reading')
        })
    )


# вариант регистрации модели без декоратора
# class BookAdmin(admin.ModelAdmin):
#     pass
# admin.site.register(Book, BookAdmin) - настройки админки для модели Book храняться в классе BookAdmin

