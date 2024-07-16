from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import BookFilter
from .models import Book, Review
from .serializers import BookListSerializer, BookDetailSerializer, ReviewSerializer


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


class ReviewCreateView(CreateAPIView):
    """
    Create a new review with book rating.
    """
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, ]

    def create(self, request, *args, **kwargs):
        book_id = self.kwargs.get('pk')
        try:
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user has already reviewed this book
        if Review.objects.filter(book=book, author=request.user).exists():
            return Response({"error": "You have already reviewed this book"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(book=book, author=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class AddToFavoriteView(APIView):
    """
    Add or remove a book from favorites.
    No content should be added to the request.
    """
    permission_classes = [IsAuthenticated, ]

    def post(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        if book.favorites.filter(id=user.id).exists():
            book.favorites.remove(user)
            return Response({"Status": "Removed from favorites"}, status=status.HTTP_200_OK)
        else:
            book.favorites.add(user)
            return Response({"Status": "Added to favorites"}, status=status.HTTP_200_OK)
