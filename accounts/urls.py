from django.urls import path
from .views import RegisterAPIView, verify_email_view
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('api/register/', RegisterAPIView.as_view(), name='api_register'),
    path('api/login/', obtain_auth_token, name='api_login'),
    path('verify-email/', verify_email_view, name='verify_email'),
]
