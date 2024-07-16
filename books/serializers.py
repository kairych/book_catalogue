from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Book, Genre, Author, Review


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['name']


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['name']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['email']


class ReviewSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['author', 'rating', 'text']


class BookListSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    author = AuthorSerializer(many=True, read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    is_favorited = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(view_name='book_detail', lookup_field='pk')

    class Meta:
        model = Book
        fields = ['title', 'genre', 'author', 'publication_date', 'average_rating', 'is_favorited', 'url']

    def get_is_favorited(self, obj):
        """
        Method shows if selected book is favorited by current user or not.
        :param obj: Book object
        :return: boolean
        """
        request = self.context.get('request', None)
        if request and request.user in obj.favorites.all():
            return True
        return False


class BookDetailSerializer(BookListSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = [
            'title',
            'description',
            'genre',
            'author',
            'publication_date',
            'is_favorited',
            'average_rating',
            'reviews',
        ]
