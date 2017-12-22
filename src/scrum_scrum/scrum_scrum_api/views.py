# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from django.conf import settings
from django.utils import timezone
from django.utils.encoding import force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode

from . import serializers
from . import permissions
from . import models
from . import activation
from .authentication import ExpiringTokenAuthentication
from .authentication import get_client

logger = logging.getLogger('django')

@api_view(['GET'])
def activate(request, user_id, activation_key):
    """This method attempts to activate a user's account."""

    try:
        user_id = force_text(urlsafe_base64_decode(user_id))
        key = force_text(urlsafe_base64_decode(activation_key))
    except (TypeError, DjangoUnicodeDecodeError):
        #   If the activation key or user id is not encoded properly or has
        #   become corrupted, just return an error rather that raising
        #   an exception
        return Response({
            "error": ("The activation link was corrupted. If copy/pasted, "
                      "make sure it was copied correctly.")
        }, status=status.HTTP_400_BAD_REQUEST)

    user = models.ScrumScrumUser.objects.get(pk=user_id)
    try:
        activation_key = models.ActivationKey.objects.get(key=key, user=user)
    except models.ActivationKey.DoesNotExist:
        #   The activation key provided is either incorrect or has been
        #   archived.
        try:
            #   Check if the key has been archived
            archived_key = models.ArchivedActivationKey.objects.get(key=key)
        except models.ArchivedActivationKey.DoesNotExist:
            #   The key wasn't archived, so something is wrong with the key.
            err = "The activation link is incorrect or has already been used."
            return Response({
                "error": err
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            #   The key was archived and the user's account was deleted.
            #   Ask them to make a new account.
            err = "The activation link is expired. Please create a new account."
            return Response({
                "error": err
            }, status=status.HTTP_400_BAD_REQUEST)

    #   The activation key exists, but we still need to make sure it hasn't
    #   expired yet.
    if activation_key.expires <= timezone.now():
        activation.archive()
        err = "The activation link has expired. Please create a new account."
        return Response({
            "error": err
        }, status=status.HTTP_400_BAD_REQUEST)

    #   The activation key exists and has not expired. Activate the user's
    #   account and delete the activation key.
    activation_key.delete()
    user.is_active = True
    user.save()

    return Response({
        "Message": "Thank you for activating your account!"
    }, status=status.HTTP_200_OK)



class ObtainExpiringAuthToken(ObtainAuthToken):
    """Returns a ScrumScrumUserToken.

    Depending on the type of client specified in the HTTP_CLIENT header,
    this will either return a token with an expiration or one without.
    Mobile-applications will get a lifetime token, while web-based clients
    will get a token that will eventually expire. Change TOKEN_EXPIRATION_DAYS
    in django.conf.settings to modify the number of days a web-client token
    will be valid.
    """

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            try:
                #   Try to get the client type ('web' or 'mobile')
                client = get_client(request)
            except ValueError as e:
                #   There was a problem with the client format in the
                #   HTTP header
                return Response({
                    "error": str(e)
                }, status=status.HTTP_400_BAD_REQUEST)

            token, created = \
                models.ScrumScrumUserToken.objects.get_or_create(user=user,
                                                                 client=client)

            if not created:
                #   We've created a new token, set the `created_on` field
                #   to the current UTC time
                token.created_on = timezone.now()
                token.save()

            #   Give the token to the client
            return Response({"token": token.key})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginViewSet(viewsets.ViewSet):
    """Verifies user credentials and returns an authentication token."""

    serializer_class = AuthTokenSerializer

    def create(self, request):
        """Use the ObtainAuthToken APIView to validate and create a token."""

        return ObtainExpiringAuthToken().post(request)

class ScrumScrumUserViewSet(viewsets.ModelViewSet):
    """Handles creating, reading, and updating scrum scrum users."""

    serializer_class = serializers.ScrumScrumNewUserSerializer
    queryset = models.ScrumScrumUser.objects.all()
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (permissions.UpdateOwnUser,)

    def get_serializer_class(self):
        """Configure the right serializer depending on URL request method.

        We want to make sure that all ScrumScrumUser fields are exposed on the
        POST method (creating new users), but we don't want current users to
        update certain information such as their username (PUT/PATCH methods).
        """
        serializer_class = self.serializer_class

        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            serializer_class = serializers.ScrumScrumUpdateUserSerializer

        return serializer_class

    def create(self, request, *args, **kwargs):
        """Override the default create method for a ModelViewSet.

        Overriding this method allows us to send a verification email
        to the email address the user entered.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        user = models.ScrumScrumUser.objects.get(
                username=serializer.data.get('username'))
        activation.send_activation_email(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)
