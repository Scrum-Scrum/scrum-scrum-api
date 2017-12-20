# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken

from . import serializers
from . import permissions
from . import models
from authentication import JWTAuthentication
# Create your views here.

import logging

class ObtainExpiringAuthToken(ObtainAuthToken):
    """Returns an auth token with an expriation."""

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token = user.token

            # Return JSON response { "token" : "<the token>" }
            return Response({"token": token})
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
    authentication_classes = (JWTAuthentication,)
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
