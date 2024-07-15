from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework.filters import OrderingFilter

from .filters import BookFilter
from .models import Book
from .serializers import BookSerializer


class BookListView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = BookFilter
    ordering_fields = ['title', 'author', 'publication_date', 'average_rating']

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(average_rating=Avg('reviews__rating'))
        return queryset
