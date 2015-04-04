# -*- coding: latin-1 -*-
from django.core.validators import RegexValidator

password_validator = RegexValidator(
    r'^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,32}$',
    message='The password must contain at least one uppercase, a lowercase letter and a number'
)
