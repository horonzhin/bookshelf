from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from books.models import Basket, Book
from books.serializers import BasketSerializer, BookSerializer


class BookModelViewSet(ModelViewSet):
    """APIView of the reader's book list"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # allow only authenticated users to access the API, except GET requests
    # permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_permissions(self):
        """Determining Permissions"""
        # if the action is create, update or delete, then only the admin can do it
        if self.action in ('create', 'update', 'destroy'):
            self.permission_classes = (IsAdminUser,)
        return super(BookModelViewSet, self).get_permissions()


class BasketModelViewSet(ModelViewSet):
    """APIView for Basket"""
    queryset = Basket.objects.all()
    serializer_class = BasketSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """The method of filtering the basket by user so that the user does not see the basket of others"""
        queryset = super(BasketModelViewSet, self).get_queryset()
        return queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """Method of adding books to the basket"""
        try:  # If an incorrect field is specified, issue an error
            book_id = request.data['book']
            books = Book.objects.filter(id=book_id)  # check if there is a book in the database
            if not books.exists():  # if the book is not in the database, we will return an error
                return Response({'book': 'There is no book with this ID.'}, status=status.HTTP_400_BAD_REQUEST)
            obj, is_created = Basket.create_or_update(books.first().id, self.request.user)
            status_code = status.HTTP_201_CREATED if is_created else status.HTTP_200_OK
            # In order to create (post) not to fill in the dict of the book, take data from the serializer
            serializer = self.get_serializer(obj)
            return Response(serializer.data, status=status_code)
        except KeyError:
            return Response({'book': 'This field is required.'}, status=status.HTTP_400_BAD_REQUEST)
