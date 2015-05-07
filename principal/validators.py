# -*- coding: latin-1 -*-
from django.core.validators import RegexValidator
from django.utils.translation import ugettext as _

password_validator = RegexValidator(
    r'^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,32}$',
    message=_('The password must contain at least one uppercase, a lowercase letter and a number')
)
