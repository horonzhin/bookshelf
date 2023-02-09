from books.models import Basket, Book


def baskets(request):
    """Global variable 'baskets' for use in all templates"""
    user = request.user
    return {'baskets': Basket.objects.filter(user=user) if user.is_authenticated else []}


def bookshelves(request):
    """Global variable 'bookshelves' for use in all templates"""
    user = request.user
    return {'bookshelves': Book.objects.filter(user=user) if user.is_authenticated else []}
