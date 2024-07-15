from django.contrib.auth import get_user_model
from rest_framework import serializers

from books.models import Book, Genre, Author, Review


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
        fields = ['id', 'username', 'email']


class ReviewSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'text', 'rating', 'author', 'created_at']


class BookSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    author = AuthorSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Book
        fields = ['title', 'author', 'genre', 'publication_date', 'average_rating', 'reviews']
