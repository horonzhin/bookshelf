from rest_framework import serializers

from books.models import Book, Author, Genre, Cycle, Series


class BookSerializer(serializers.ModelSerializer):
    """Serializer for Book model"""
    # show the name from the ForeignKey/ManyToMany field in the API instead of the ID
    author = serializers.SlugRelatedField(slug_field='last_name', many=True, queryset=Author.objects.all())
    genre = serializers.SlugRelatedField(slug_field='name', many=True, queryset=Genre.objects.all())
    cycle = serializers.SlugRelatedField(slug_field='name', queryset=Cycle.objects.all())
    series = serializers.SlugRelatedField(slug_field='name', queryset=Series.objects.all())

    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'cover', 'isbn', 'published', 'genre',
                  'cycle', 'series', 'annotation', 'price', 'category', 'text')