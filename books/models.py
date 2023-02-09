import stripe

from django.conf import settings
from django.db import models

from users.models import User

stripe.api_key = settings.STRIPE_SECRET_KEY


class BookCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


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


class Book(models.Model):
    READING = 0
    FINISHED = 1
    TO_READ = 2
    INTEREST = 3
    DROPPED = 4
    STATUSES = (
        (READING, 'Читаю'),
        (FINISHED, 'Закончена'),
        (TO_READ, 'Буду читать'),
        (INTEREST, 'Заинтересовала'),
        (DROPPED, 'Заброшена'),
    )

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
    status = models.SmallIntegerField(choices=STATUSES, default=FINISHED, verbose_name='Статус')
    rating = models.SmallIntegerField(choices=((0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'),),
                                      default=0, verbose_name='Рейтинг')
    first_reading = models.DateField(blank=True, default=None, null=True, verbose_name='Первое прочтение')
    second_reading = models.DateField(blank=True, default=None, null=True, verbose_name='Второе прочтение')
    third_reading = models.DateField(blank=True, default=None, null=True, verbose_name='Третье прочтение')
    price = models.DecimalField(blank=True, default=None, null=True, max_digits=8, decimal_places=2)
    category = models.ForeignKey(BookCategory, blank=True, default=None, null=True, on_delete=models.CASCADE,
                                 related_name='book', verbose_name='Категория')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='book', verbose_name='Читатель')
    stripe_book_price_id = models.CharField(max_length=128, null=True, blank=True,
                                            verbose_name='Price id книги в Stripe')
    text = models.FileField(upload_to='book_texts', blank=True, default=None, null=True, verbose_name='Текст книги')

    def get_author(self):
        """To display authors in the admin panel list_display"""
        return ",".join([str(p) for p in self.author.all()])

    def get_genre(self):
        """To display genres in the admin panel list_display"""
        return ",".join([str(p) for p in self.genre.all()])

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """Before saving to the database, if the author's books have an empty stripe_product_price field,
        load the price from stripe via the API"""
        # todo = сделать так чтобы stripe_book_price_id сохранялся только у книг автора
        if not self.stripe_book_price_id:
            stripe_product_price = self.create_stripe_product_price()
            self.stripe_book_price_id = stripe_product_price['id']
        super(Book, self).save(force_insert=False, force_update=False, using=None, update_fields=None)

    def create_stripe_product_price(self):
        """
        Create a product (book) price in stripe:
        1. Create a product in stripe
        2. Create a price for the product in stripe
        """
        stripe_product = stripe.Product.create(name=self.title)
        stripe_product_price = stripe.Price.create(
            product=stripe_product['id'],
            unit_amount=round(self.price * 100),  # indicate the amount in kopecks
            currency="rub"
        )
        return stripe_product_price

    class Meta:
        ordering = ['title']
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    def __str__(self):
        return self.title


class BasketQuerySet(models.QuerySet):
    """
    Create our own methods in the basket queryset to call them in templates.
    Regular queryset methods cannot be called in templates
    """
    def total_sum(self):
        """Total sum of books in the basket"""
        return sum(basket.sum() for basket in self)

    def total_quantity(self):
        """Total quantity of books in the basket"""
        return sum(basket.quantity for basket in self)

    def stripe_products(self):
        """Fill in the data (price and quantity) for stripe"""
        line_items = []
        for basket in self:
            item = {
                'price': basket.book.stripe_book_price_id,
                'quantity': basket.quantity,
            }
            line_items.append(item)
        return line_items


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    # when we access Basket.objects.all() we will complement it with our queryset with our methods from BasketQuerySet
    objects = BasketQuerySet.as_manager()

    def sum(self):
        """Total sum of books"""
        return self.book.price * self.quantity

    def de_json(self):
        """Returns a dictionary with data about the basket to save the history of orders"""
        basket_item = {
            'product_name': self.book.title,
            'quantity': self.quantity,
            'price': float(self.book.price),
            'sum': float(self.sum()),
        }
        return basket_item

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return f'Корзина для {self.user.username} | Книга: {self.book.title}'


# class BookReview(models.Model):
#     user_name = models.CharField(max_length=30)
#     text = models.TextField(max_length=3000)
#     review = models.ForeignKey(Book, default=None, null=True, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, default=None, null=True, on_delete=models.CASCADE)
#
#     class Meta:
#         verbose_name = 'Рецензия'
#         verbose_name_plural = 'Рецензии'
