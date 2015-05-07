# -*- coding: utf-8 -*-
from django.template.loader import render_to_string
from django.core.mail.message import EmailMessage
import hashlib
from django.utils import translation


def send_email_confirmation(traveller, rand_password):
    hash_confirm = hashlib.sha256(traveller.username).hexdigest()
    if translation.get_language() == "es":
        send_templated_email = render_to_string('email/register_confirmation_es.html',
                                                {'hash': hash_confirm, 'username': traveller.username,
                                                 'name': traveller.first_name,
                                                 'rand_password': rand_password})
        email = EmailMessage('Welcome to BrainTravel', send_templated_email, to=[traveller.email])
        email.content_subtype = "html"
        email.send()
    else:
        send_templated_email = render_to_string('email/register_confirmation_en.html',
                                                {'hash': hash_confirm, 'username': traveller.username,
                                                 'name': traveller.first_name,
                                                 'rand_password': rand_password})
        email = EmailMessage('Welcome to BrainTravel', send_templated_email, to=[traveller.email])
        email.content_subtype = "html"
        email.send()