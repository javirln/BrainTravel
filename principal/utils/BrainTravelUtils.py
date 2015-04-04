# -*- coding: latin-1 -*-
import random
import string
from django.contrib import messages
from django.utils.translation import ugettext as _

def id_generator(size=6, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def save_info(request, message_code):
    messages.add_message(request, messages.INFO, _(message_code))

def save_success(request, message_code):
    messages.add_message(request, messages.SUCCESS, _(message_code))
    
def save_warning(request, message_code):
    messages.add_message(request, messages.WARNING, _(message_code))
    
def save_error(request, message_code=None):
    if message_code is None:
        message_code = 'An unexpected error has occurred'
    messages.add_message(request, messages.ERROR, _(message_code))
    