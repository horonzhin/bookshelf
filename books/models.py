from django.contrib.auth.models import User
from django.db import models
from users.models import User


class Genre(models.Model):
    name = models.CharField(max_length=100, verbose_name='Жанр')

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(max_length=100, default=None, null=True, verbose_name='Имя')
    last_name = models.CharField(max_length=100, default=None, null=True, verbose_name='Фамилия')
    birthday = models.DateField(blank=True, default=None, null=True, verbose_name='Дата рождения')
    death = models.DateField(blank=True, default=None, null=True, verbose_name='Дата смерти')
    country = models.CharField(max_length=100, blank=True, default=None, null=True, verbose_name='Страна')

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

    def __str__(self):
        return f'{self.last_name} {self.first_name}'


class Cycle(models.Model):
    name = models.CharField(max_length=100, verbose_name='Цикл')

    class Meta:
        verbose_name = 'Цикл'
        verbose_name_plural = 'Циклы'

    def __str__(self):
        return self.name


class Series(models.Model):
    name = models.CharField(max_length=100, verbose_name='Серия')

    class Meta:
        verbose_name = 'Серия'
        verbose_name_plural = 'Серии'

    def __str__(self):
        return self.name


class Status(models.Model):
    name = models.CharField(max_length=100, verbose_name='Статус')

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=100, db_index=True, verbose_name='Название')
    author = models.ManyToManyField(Author, related_name='book', verbose_name='Автор')
    cover = models.ImageField(upload_to='book_covers', verbose_name='Обложка')
    isbn = models.BigIntegerField(db_index=True, verbose_name='ISBN')
    published = models.DateField(blank=True, default=None, null=True, verbose_name='Дата публикации')
    genre = models.ManyToManyField(Genre, related_name='book', verbose_name='Жанр')
    cycle = models.ForeignKey(Cycle, blank=True, default=None, null=True, on_delete=models.CASCADE,
                              related_name='book', verbose_name='Цикл')
    series = models.ForeignKey(Series, blank=True, default=None, null=True, on_delete=models.CASCADE,
                               related_name='book', verbose_name='Серия')
    annotation = models.TextField(verbose_name='Аннотация')
    status = models.ForeignKey(Status, on_delete=models.CASCADE, related_name='book', verbose_name='Статус')
    rating = models.IntegerField(blank=True, default=None, null=True, verbose_name='Рейтинг')
    first_reading = models.DateField(blank=True, default=None, null=True, verbose_name='Первое прочтение')
    second_reading = models.DateField(blank=True, default=None, null=True, verbose_name='Второе прочтение')
    third_reading = models.DateField(blank=True, default=None, null=True, verbose_name='Третье прочтение')

    class Meta:
        ordering = ['title']
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    def __str__(self):
        return self.title


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return f'Корзина для {self.user.email} | Книга: {self.book.title}'


# class Review(models.Model):
#     user_name = models.CharField(max_length=30)
#     text = models.TextField(max_length=3000)
#     review = models.ForeignKey(Book, default=None, null=True, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, default=None, null=True, on_delete=models.CASCADE)
#
#     class Meta:
#         verbose_name = 'Рецензия'
#         verbose_name_plural = 'Рецензии'
