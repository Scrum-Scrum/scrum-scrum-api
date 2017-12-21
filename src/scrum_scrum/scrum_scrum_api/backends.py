"""
This file houses the custom authentication backend that allows users to
authenticate with either email or username.
"""

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import exceptions

from .models import ScrumScrumUser

class ScrumScrumAuthBackend(ModelBackend):

    def authenticate(self, username=None, password=None, **kwargs):
        """Attempt to authenticate the user with the provided credentials."""

        user_model = get_user_model()

        if username is None:
            username = kwargs.get(user_model.USERNAME_FIELD)

        users = user_model._default_manager.filter(
            Q(**{user_model.USERNAME_FIELD: username}) |
            Q(email__iexact=username)
        )

        if not users:
            raise exceptions.AuthenticationFailed(
                'Username or email provided was not found.')

        for user in users:
            if user.check_password(password):
                return user

        raise exceptions.AuthenticationFailed(
            'Could not authenticate with provided credentials.')
