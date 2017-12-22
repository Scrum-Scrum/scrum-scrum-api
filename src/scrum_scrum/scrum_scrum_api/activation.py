"""
This file deals with user account activation.

Aside from the actual activate endpoint, which is handled in views.py,
the methods in this file will handle all activation-based operations.
"""

import random
import string
import datetime

from django.conf import settings
from django.utils import timezone
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from . import models

def gen_key():
    """Generate an ascii activation key."""

    key = ''.join(
            random.choice(string.ascii_letters + string.digits)
            for _ in range(settings.ACTIVATION_KEY_LENGTH))
    return key

def get_activation_key(user):
    """Save and return a new activation key for `user`."""

    key = gen_key()
    lifespan = datetime.timedelta(
                days=settings.ACTIVATION_KEY_EXPIRATION_DAYS)
    expires = timezone.now() + lifespan

    new_activation_key = models.ActivationKey(key=key,
                                              user=user,
                                              expires=expires)
    new_activation_key.save()
    return new_activation_key

def send_activation_email(user):
    """Send an activation email to `user`.

    This method formats an email message that includes a link to activate
    a user's new account, and sends the email to the new user's provided
    email address.
    """

    activation_key = get_activation_key(user)
    user_id_encoded = urlsafe_base64_encode(force_bytes(user.id))
    activation_key_encoded = urlsafe_base64_encode(
                                force_bytes(activation_key.key))
    url = '127.0.0.1:8080/api/activate/{}/{}'.format(
            user_id_encoded, activation_key_encoded)

    email_address = user.email
    email_subject = 'Activate your Scrum-Scrum account'
    email_body = render_to_string('activation_email.html', {
        'first_name': user.first_name,
        'activation_url': url
    })

    email = EmailMessage(email_subject, email_body, to=[email_address])
    email.send()

def archive():
    """Archive expired activation keys and delete user accounts."""

    expired_keys = models.ActivationKey.objects.filter(
                    expires__lte=timezone.now())
    keys_to_archive = []
    users_to_delete = []

    for expired in expired_keys:
        keys_to_archive.append(expired.key)
        users_to_delete.append(expired.user)
        expired.delete()

    for key in keys_to_archive:
        archived = models.ArchivedActivationKey(key=key)
        archived.save()

    for user in users_to_delete:
        user.delete()
