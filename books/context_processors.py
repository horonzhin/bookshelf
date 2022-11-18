from books.models import Basket, Book


def baskets(request):
    user = request.user
    return {'baskets': Basket.objects.filter(user=user) if user.is_authenticated else []}


def bookshelves(request):
    user = request.user
    return {'bookshelves': Book.objects.filter(user=user) if user.is_authenticated else []}
