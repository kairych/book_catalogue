import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models


class SystemUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class SystemUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name='Email')
    is_staff = models.BooleanField(default=False, verbose_name='Staff')
    is_email_confirmed = models.BooleanField(default=False, verbose_name='Is email confirmed')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Date and time of creation')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Date and time of update')

    USERNAME_FIELD = 'email'
    objects = SystemUserManager()


class EmailConfirmationToken(models.Model):
    user = models.OneToOneField(SystemUser, on_delete=models.CASCADE, related_name='email_verification_token')
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)
