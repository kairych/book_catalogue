from django.conf import settings
from django.core.mail import send_mail


def send_verification_email(url: str, email: str) -> None:
    """
    Method to send email to verify user's email address.

    :param url: verification link
    :param email: user's email address
    """
    send_mail(
        subject='Verify your email address',
        message=f'Click the link to verify your email address: {url}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )
