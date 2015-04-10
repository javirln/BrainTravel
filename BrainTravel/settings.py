"""
Django settings for BrainTravel project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'wt25dtpbzg9ks8l891^2f+hui6uqux&2s*)9@jxj20i9%=q98s'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

FILE_CHARSET = 'iso-8859-1'


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'principal',
    'django_summernote',
    'bootstrap3_datetime',
    'paypal.standard.ipn',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)

#Dir for i18n
LOCALE_PATHS = (
                os.path.join(BASE_DIR, "locale"),
                )


ROOT_URLCONF = 'BrainTravel.urls'

WSGI_APPLICATION = 'BrainTravel.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
     'default': {
         'ENGINE': 'django.db.backends.mysql',
         'NAME': 'braintravel',
         'USER': 'braintravel',
         'PASSWORD': 'bR@1nTr@veL',
         'HOST': '127.0.0.1',
         'PORT': '3306',
         'ATOMIC_REQUESTS': 'True'
     }
}

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, "/principal/templates"),
    os.path.join(BASE_DIR, "/principal/emailTemplates"),
)

# configuracion del summernote
SUMMERNOTE_CONFIG = {
    # Using SummernoteWidget - iframe mode
    'iframe': True,  # or set False to use SummernoteInplaceWidget - no iframe mode

    # Using Summernote Air-mode
    'airMode': True,

    # Use native HTML tags (`<b>`, `<i>`, ...) instead of style attributes
    # (Firefox, Chrome only)
    'styleWithTags': True,

    # Change editor size
    'width': '150%',
    'height': '480',

    # Customize toolbar buttons
    'toolbar': [
        ['style', ['style']],
        ['style', ['bold', 'italic', 'underline', 'clear', 'remove Font Style']],
        ['fontname', ['fontname']],
        ['fontsize', ['fontsize']],
        ['para', ['ul', 'ol', 'height']],
        ['insert', ['link']],
        ['color', ['color']],
    ],

    # Use proper language setting automatically (default)
    # 'lang': None
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

LOGIN_URL = '/signin/'
LOGIN_REDIRECT_URL = '/signin/'


EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'notificaciones.braintravel@gmail.com'
EMAIL_HOST_PASSWORD = 'braintravelredmine'

#PAYPAL CONFIGURATION
PAYPAL_RECEIVER_EMAIL = 'notificaciones.braintravel-facilitator@gmail.com'
PAYPAL_TEST = True


