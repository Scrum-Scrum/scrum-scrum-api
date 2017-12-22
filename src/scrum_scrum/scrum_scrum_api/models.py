# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import binascii
import os
import logging

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager

logger = logging.getLogger('django')

@python_2_unicode_compatible
class ScrumScrumUserToken(models.Model):
    """A custom Token class.

    This implementation includes the client type for which the
    token is created. The rest of the class is identical to Django REST
    framework's Token, found at
    https://github.com/encode/django-rest-framework/blob/master/rest_framework/authtoken/models.py
    """

    key = models.CharField(_("Key"), max_length=40,
                           primary_key=True)
    user = models.ForeignKey('ScrumScrumUser', on_delete=models.CASCADE)
    created_on = models.DateTimeField(_("Created"), auto_now=True)
    client = models.CharField(max_length=10)

    class Meta:
        verbose_name = _("Token")
        verbose_name_plural = _("Tokens")

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(ScrumScrumUserToken, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key

class ScrumScrumUserManager(BaseUserManager):
    """Helps Django work with the custom user model."""

    def create_user(self, email, username, first_name, last_name, password):
        """Creates a new ScrumScrumUser."""

        if not email or not username or not first_name or not last_name \
                or not password:
            raise ValueError(
                "email, username, first name, last name and password "
                + "are all required.")

        email = self.normalize_email(email)
        user = self.model(email=email,
                          username=username,
                          first_name=first_name,
                          last_name=last_name)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, username,
                         first_name, last_name, password):
        """Creates and saves a new superuser."""

        user = self.create_user(email,
                                username,
                                first_name,
                                last_name,
                                password)
        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user


class ScrumScrumUser(AbstractBaseUser, PermissionsMixin):
    """Represents a user in the world of scrum-scrum."""

    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date_joined = models.DateTimeField(auto_now=True)

    #   is_active will default to False, because users will need to
    #   verify their email address.
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = ScrumScrumUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def get_full_name(self):
        """Get the user's first and last name."""

        return self.first_name + ' ' + self.last_name

    def get_short_name(self):
        """Get the user's first name only."""

        return self.first_name

    def __str___(self):
        return self.username

class ActivationKey(models.Model):
    """This model will represent an activation key.

    Users need to verify their email with the correct activation key.
    """

    lifespan = datetime.timedelta(
                seconds=settings.ACTIVATION_KEY_EXPIRATION_DAYS)

    key = models.CharField(
            max_length=settings.ACTIVATION_KEY_LENGTH)
    user = models.ForeignKey(ScrumScrumUser, related_name='scrum_scrum_user',
                             on_delete=models.CASCADE)
    expires = models.DateTimeField()

    class Meta:
        unique_together = (('key', 'user'),)

class ArchivedActivationKey(models.Model):
    """This model will represent an activation key that has expired."""

    key = models.CharField(
            max_length=settings.ACTIVATION_KEY_LENGTH, unique=True)
