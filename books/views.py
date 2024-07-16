from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated

from .filters import BookFilter
from .models import Book
from .serializers import BookListSerializer, BookDetailSerializer


class BookListView(ListAPIView):
    """
    Show all books.

    Items can be filtered by genre, author or publication date,
    or can be ordered by book title, author, publication date and average rating.
    *Publication date is shown in a books list to see dates for filtering.
    """
    queryset = Book.objects.all()
    serializer_class = BookListSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = BookFilter
    ordering_fields = ['title', 'author', 'publication_date', 'average_rating']

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(average_rating=Avg('reviews__rating'))
        return queryset


class BookDetailView(RetrieveAPIView):
    """
    Show book details including book description, reviews and ratings.
    Book details are accessible only to authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookDetailSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(average_rating=Avg('reviews__rating')) # Calculate average rating for selected book
        return queryset
