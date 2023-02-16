from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser

from books.models import Book
from books.serializers import BookSerializer


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
