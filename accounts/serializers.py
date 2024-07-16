from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import SystemUser


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        style={'placeholder': '*Email Address'},
        help_text="Required",
        validators=[UniqueValidator(queryset=SystemUser.objects.all())]
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password', 'placeholder': '*Password'},
        help_text="Required",
        validators=[validate_password],
    )
    confirm_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password', 'placeholder': '*Confirm password'},
        help_text="Required",
    )

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'password', 'confirm_password')
        extra_kwargs = {
            'email': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = SystemUser.objects.create_user(
            email=validated_data['email'],
        )
        return user
