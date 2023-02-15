from rest_framework.generics import ListAPIView

from books.models import Book
from books.serializers import BookSerializer


class BookListAPIView(ListAPIView):
    """APIView of the reader's book list"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
