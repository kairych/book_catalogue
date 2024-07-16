from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView, get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .helpers import send_verification_email
from .models import EmailConfirmationToken, SystemUser
from .serializers import RegisterSerializer


class RegisterAPIView(CreateAPIView):
    """
    Register a new user.

    Please, provide valid email and password.
    Password must be confirmed.
    Verification email is sent upon registration.
    """
    queryset = SystemUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny, )

    def perform_create(self, serializer):
        user = serializer.save()
        token = EmailConfirmationToken.objects.create(user=user)
        self.send_verification_email(user.email, token.token)

    @staticmethod
    def send_verification_email(email, token):
        verification_url = f'{settings.FRONTEND_URL}/accounts/verify-email/?token={token}'
        send_verification_email(verification_url, email)


@swagger_auto_schema(
    manual_parameters=[
        openapi.Parameter('token', openapi.IN_QUERY, description="Email verification token", type=openapi.TYPE_STRING)
    ],
    responses={
        200: openapi.Response(
            'Email confirmed',
            examples={"application/json": {"Status": "Email has been confirmed."}}
        ),
        400: openapi.Response(
            'Email already confirmed or invalid token',
            examples={"application/json": {"Status": "Email has already been verified."}}
        ),
    }
)
@csrf_exempt
def verify_email_view(request) -> JsonResponse:
    """
    View to verify user's email.
    """
    token = request.GET.get('token', None)

    try:
        user_token = get_object_or_404(EmailConfirmationToken, token=token)
        user = user_token.user  # Find user by token
        if user.is_email_confirmed:  # Check if email is already confirmed, return corresponding response
            data = {"Status": "Email has already been verified."}
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
        user.is_email_confirmed = True  # Confirm email by setting parameter to True
        user.save()
        user_token.delete()  # Delete token after confirmation of user's email
        data = {"Status": "Email has been confirmed."}
        return JsonResponse(data, status=status.HTTP_200_OK)
    except EmailConfirmationToken.DoesNotExist:
        data = {"Status": "Email is not confirmed."}
        return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
