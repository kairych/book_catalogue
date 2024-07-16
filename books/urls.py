from django.urls import path, include
from .views import BookListView, BookDetailView, ReviewCreateView, AddToFavoriteView

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('', BookListView.as_view(), name='book_list'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('books/<int:pk>/reviews/', ReviewCreateView.as_view(), name='review_create'),
    path('books/<int:pk>/toggle_favorite/', AddToFavoriteView.as_view(), name='toggle_favorite'),
]
