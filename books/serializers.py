from rest_framework import fields, serializers

from books.models import Author, Basket, Book, Cycle, Genre, Series


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


class BasketSerializer(serializers.ModelSerializer):
    """Serializer for Basket"""
    book = BookSerializer()  # show data about the book taken from BookSerializer
    sum = fields.FloatField(required=False)  # show the data from the method we created (sum) in the basket model
    total_sum = fields.SerializerMethodField()  # show the data from the serializer method
    total_quantity = fields.SerializerMethodField()

    def get_total_sum(self, obj):
        """Method for displaying the total sum of the basket"""
        return Basket.objects.filter(user_id=obj.user_id).total_sum()

    def get_total_quantity(self, obj):
        """Method for displaying the total quantity of the basket"""
        return Basket.objects.filter(user_id=obj.user_id).total_quantity()

    class Meta:
        model = Basket
        fields = ('id', 'book', 'quantity', 'sum', 'total_sum', 'total_quantity', 'created_timestamp')
        read_only_fields = ('created_timestamp',)
