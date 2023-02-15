from rest_framework import serializers

from books.models import Book


class BookSerializer(serializers.ModelSerializer):
    """Serializer for Book model"""
    # show the name from the ForeignKey/ManyToMany field in the API instead of the ID
    author = serializers.SlugRelatedField(slug_field='last_name', read_only=True, many=True)
    genre = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    cycle = serializers.SlugRelatedField(slug_field='name', read_only=True)
    series = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'cover', 'isbn', 'published', 'genre',
                  'cycle', 'series', 'annotation', 'price', 'category', 'text')