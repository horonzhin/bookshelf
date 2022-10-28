from django.contrib.auth.models import User
from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=100, verbose_name='Жанр')

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=100, verbose_name='Автор')

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

    def __str__(self):
        return self.name


class Cycle(models.Model):
    name = models.CharField(max_length=100, verbose_name='Цикл')

    class Meta:
        verbose_name = 'Цикл'
        verbose_name_plural = 'Циклов'

    def __str__(self):
        return self.name


class Series(models.Model):
    name = models.CharField(max_length=100, verbose_name='Серия')

    class Meta:
        verbose_name = 'Серия'
        verbose_name_plural = 'Серий'

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
    cover = models.ImageField(upload_to='books_cover', verbose_name='Обложка')
    author = models.ManyToManyField(Author, related_name='book', verbose_name='Автор')
    isbn = models.IntegerField(max_length=30, db_index=True, verbose_name='ISBN')
    published = models.DateTimeField(default=None, null=True, verbose_name='Дата публикации')
    genre = models.ManyToManyField(Genre, related_name='book', verbose_name='Жанр')
    cycle = models.ForeignKey(Cycle, default=None, null=True, on_delete=models.CASCADE,
                              related_name='book', verbose_name='Цикл')
    series = models.ForeignKey(Series, default=None, null=True, on_delete=models.CASCADE,
                               related_name='book', verbose_name='Серия')
    status = models.ForeignKey(Status, on_delete=models.CASCADE, related_name='book', verbose_name='Статус')
    first_reading = models.DateTimeField(default=None, null=True, verbose_name='Первое прочтение')
    second_reading = models.DateTimeField(default=None, null=True, verbose_name='Второе прочтение')
    third_reading = models.DateTimeField(default=None, null=True, verbose_name='Третье прочтение')
    rating = models.IntegerField(default=None, null=True, verbose_name='Рейтинг')
    annotation = models.TextField(verbose_name='Аннотация')

    class Meta:
        db_table = 'Книги'
        ordering = ['title']
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    def __str__(self):
        return self.title
#
#
# class Review(models.Model):
#     user_name = models.CharField(max_length=30)
#     text = models.TextField(max_length=3000)
#     review = models.ForeignKey(Book, default=None, null=True, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, default=None, null=True, on_delete=models.CASCADE)
#
#     class Meta:
#         verbose_name = 'Рецензия'
#         verbose_name_plural = 'Рецензии'
