# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager

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
    is_active = models.BooleanField(default=True)
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
