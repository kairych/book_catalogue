from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Book, Genre, Author, Review


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email']


class ReviewSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['text', 'rating', 'author', 'created_at']


class BookListSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    author = AuthorSerializer(many=True, read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name='book_detail', lookup_field='pk')

    class Meta:
        model = Book
        fields = ['title', 'author', 'genre', 'publication_date', 'average_rating', 'url']


class BookDetailSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    author = AuthorSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Book
        fields = ['title', 'author', 'genre', 'publication_date', 'average_rating', 'reviews']

