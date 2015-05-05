# -*- coding: utf-8 -*-
from django.template.context import Context
from django.template.loader import render_to_string
from django.core.mail.message import EmailMessage
import hashlib


def send_email_confirmation(traveller, rand_password):
    hash_confirm = hashlib.sha256(traveller.username).hexdigest()
    send_templated_email = render_to_string('email/register_confirmation.html',
                                            {'hash': hash_confirm, 'username': traveller.first_name,
                                             'rand_password': rand_password})
    email = EmailMessage('Welcome to BrainTravel', send_templated_email, to=[traveller.email])
    email.content_subtype = "html"
    email.send()