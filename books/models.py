from django.db import models

# class Genre(models.Model):
#     name = models.CharField(max_length=100, verbose_name='Жанр')
#
#     class Meta:
#         verbose_name = 'Жанр'
#         verbose_name_plural = 'Жанры'
#
#     def __str__(self):
#         return self.name
#
#
# class Author(models.Model):
#     name = models.CharField(max_length=100, verbose_name='Автор')
#
#     class Meta:
#         verbose_name = 'Автор'
#         verbose_name_plural = 'Авторы'
#
#     def __str__(self):
#         return self.name
#
#
# class Cycle(models.Model):
#     name = models.CharField(max_length=100, verbose_name='Цикл')
#
#     class Meta:
#         verbose_name = 'Цикл'
#         verbose_name_plural = 'Циклов'
#
#     def __str__(self):
#         return self.name
#
#
# class Series(models.Model):
#     name = models.CharField(max_length=100, verbose_name='Серия')
#
#     class Meta:
#         verbose_name = 'Серия'
#         verbose_name_plural = 'Серий'
#
#     def __str__(self):
#         return self.name
#
#
# class Status(models.Model):
#     name = models.CharField(max_length=100, verbose_name='Статус')
#
#     class Meta:
#         verbose_name = 'Статус'
#         verbose_name_plural = 'Статусы'
#
#     def __str__(self):
#         return self.name
#
#
# class Book(models.Model):
#     title = models.CharField(max_length=100, db_index=True, verbose_name='Название')
#     annotation = models.TextField(default=None, null=True, verbose_name='Аннотация')
#     published = models.DateTimeField(default=None, null=True, verbose_name='Дата публикации')
#     genre = models.ManyToManyField(Genre, default=None, null=True, on_delete=models.CASCADE,
#                                    related_name='book', verbose_name='Жанр')
#     author = models.ManyToManyField(Author, default=None, null=True, on_delete=models.CASCADE,
#                                     related_name='book', verbose_name='Автор')
#     cycle = models.ForeignKey(Cycle, default=None, null=True, on_delete=models.CASCADE,
#                               related_name='book', verbose_name='Цикл')
#     series = models.ForeignKey(Series, default=None, null=True, on_delete=models.CASCADE,
#                                related_name='book', verbose_name='Серия')
#     status = models.ForeignKey(Status, default=None, null=True, on_delete=models.CASCADE,
#                                related_name='book', verbose_name='Статус')
