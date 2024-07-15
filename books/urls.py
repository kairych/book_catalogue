from django.urls import path, include
from rest_framework import routers

from .views import BookListView, BookViewSet


router = routers.DefaultRouter()
router.register(r'books', BookViewSet, basename='books')

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('', include(router.urls)),
]
