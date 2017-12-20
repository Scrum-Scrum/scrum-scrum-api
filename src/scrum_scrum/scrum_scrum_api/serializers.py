from rest_framework import serializers

from . import models

class ScrumScrumNewUserSerializer(serializers.ModelSerializer):
    """A serializer for a new ScrumScrumUser object."""

    class Meta:
        model = models.ScrumScrumUser
        fields = (
            'id', 'email', 'username', 'first_name', 'last_name', 'password',
            'date_joined', 'is_active',
        )
        extra_kwargs = {
            'password': {'write_only': True},
            'is_active': {'read_only': True},
        }

    def create(self, validated_data):
        """Create and return a new ScrumScrumUser."""

        user = models.ScrumScrumUser(email=validated_data['email'],
                                     username=validated_data['username'],
                                     first_name=validated_data['first_name'],
                                     last_name=validated_data['last_name'])
        user.set_password(validated_data['password'])
        user.save()

        return user

class ScrumScrumUpdateUserSerializer(serializers.ModelSerializer):
    """A serializer for updating ScrumScrumUser objects."""

    class Meta:
        model = models.ScrumScrumUser
        fields = (
            'id', 'email', 'first_name', 'last_name',
            'date_joined', 'is_active',
        )
        extra_kwargs = {
            'is_active': {'read_only': True},
        }
