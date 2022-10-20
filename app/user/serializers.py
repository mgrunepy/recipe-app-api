"""
Serializers for the user API View
"""
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create and return a user with encrypted password"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update and return user"""
        # Take the password out of the validated data using pop
        # If no password set in the validated data, default to None
        password = validated_data.pop('password', None)

        # Use the parent class update method to update the user
        user = super().update(instance, validated_data)

        # Handle password update ourselves
        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token"""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    # Validate method gets called at the validation stage by the view
    def validate(self, attrs):
        """Validate and authenticate the user"""
        # Get user values
        email = attrs.get('email')
        password = attrs.get('password')
        # Authenticate user.  Request is required for function
        # although not necessarily needed in this case.
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        # If user was not set validation failed
        if not user:
            msg = _('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')

        # If user was set
        attrs['user'] = user
        return attrs
