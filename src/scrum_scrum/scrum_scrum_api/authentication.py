import datetime
import logging

from django.conf import settings
from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication
from rest_framework.authentication import get_authorization_header
from django.utils import timezone

from .models import ScrumScrumUserToken

logger = logging.getLogger('django')

def get_client(request):
    """Extract the client type from the HTTP header.

    Clients should include the following in the HTTP request header:
        HTTP_CLIENT: <client_type>  <-- Could be either web or mobile

    NOTE: it is acceptable to format the header like so:
        client: <client_type>  <-- Could be either web or mobile

        Django will automagically transform 'client' to 'HTTP_CLIENT'.
    """

    client = request.META.get('HTTP_CLIENT', b'')
    if not isinstance(client, str):
        raise ValueError('HTTP_CLIENT must be a string.')

    if client not in ('web', 'mobile'):
        raise ValueError('Unknown HTTP_CLIENT in Authorization Header.')

    return client

def update_password(user, serialized_data):
    """Update a user's password if they provide the correct current password."""

    current_password = serialized_data.get('current_password')
    new_password = serialized_data.get('new_password')
    if not user.check_password(current_password):
        raise exceptions.AuthenticationFailed("Current password is incorrect")

    user.set_password(new_password)
    user.save()


class ExpiringTokenAuthentication(TokenAuthentication):

    model = ScrumScrumUserToken

    def authenticate(self, request):
        """Override TokenAuthentication base implementation.

        This overridden method will determine the type of client
        ('web', 'mobile') that is trying to authenticate. This matters
        because mobile apps' tokens will never expire, while web-based
        tokens will expire.
        """

        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = _('Invalid token header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid token header. '
                    'Token string contains too many spaces.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = _('Invalid token header. '
                    'Token string should not contain invalid characters.')
            raise exceptions.AuthenticationFailed(msg)

        client = get_client(request)

        return self.authenticate_credentials(token, client)

    def authenticate_credentials(self, key, client):
        """Actually authenticate the given credentials."""

        try:
            token = self.get_model().objects.get(key=key)
        except self.get_model().DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token')
        except self.get_model().MultipleObjectsReturned:
            raise exceptions.AuthenticationFailed('Multiple matching tokens')

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed(
                'User is inactive or deleted their account.')

        #   Check the timestamp on the token to see if it's expired.
        #   Only do this if a web client is trying to authenticate.
        if client == 'web':
            utc_now = timezone.now()
            expire = datetime.timedelta(days=settings.TOKEN_EXPIRATION_DAYS)
            if token.created_on < utc_now - expire:
                raise exceptions.AuthenticationFailed('Token has expired')

        return token.user, token
