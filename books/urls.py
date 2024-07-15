from django.urls import path, include

from .views import BookListView


urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('', BookListView.as_view(), name='book_list'),
]
