from django.contrib import admin
from books.models import Status, Genre, Author, Cycle, Series, Book, BookCategory, Basket


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
        }),
        ('Категории', {
            'fields': ('category',)
        })
    )


class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('book', 'quantity', 'created_timestamp')
    readonly_fields = ('created_timestamp',)
    extra = 0

