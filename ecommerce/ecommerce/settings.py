import os
import logging
import logging.config
from datetime import timedelta
from pathlib import Path
import environ
import dj_database_url
from django.contrib import messages

BASE_DIR = Path(__file__).resolve().parent.parent # the project directory, where manage.py is located

PROJECT_NAME = 'ReFRESH'

# configure the environment for development
#env = environ.Env()use this in development
#env.read_env(BASE_DIR.parent / '.env') use this in development

SECRET_KEY = os.environ('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ('DEBUG')

ALLOWED_HOSTS = ['refresh.up.railway.app'] 
CSRF_TRUSTED_ORIGINS = ['refresh.up.railway.app']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'whitenoise.runserver_nostatic', # for static files
    'debug_toolbar',

    #third party libraries
   
    'sorl.thumbnail',
    'mathfilters',
    'crispy_forms',
    'crispy_bootstrap5',
    'django_email_verification',
    #'django_celery_beat',
    'django_celery_results',
    'django_htmx',
    'rest_framework',
    'djoser',
    'drf_yasg',
    


    #apps 
    'store.apps.StoreConfig',
    'cart.apps.CartConfig',
    'account.apps.AccountConfig',
    'payment.apps.PaymentConfig',
    'reviews.apps.ReviewsConfig',
    
    'api.apps.ApiConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    
]

ROOT_URLCONF = 'ecommerce.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'store.context_processor.categories', #retrieves all product categories in a context dict to display in the base template 
                'cart.context_processor.get_cart', # retrieves a cart instance in a context dict
            ],
        },
    },
]

WSGI_APPLICATION = 'ecommerce.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(default=os.environ('DB_URL'))
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'CET'

USE_I18N = True

USE_TZ = True

# login url for the login_required redirects:
LOGIN_URL = 'account:login'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'  
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = BASE_DIR / 'static'  # handled by whitenoise

MEDIA_URL = '/media/' # handle user-uploaded files 
MEDIA_ROOT = BASE_DIR / 'media' # handle user-uploaded files 

MESSAGE_TAGS = {
        messages.DEBUG: 'alert-secondary',
        messages.INFO: 'alert-info',
        messages.SUCCESS: 'alert-success',
        messages.WARNING: 'alert-warning',
        messages.ERROR: 'alert-danger',
 }


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Needed for the debug toolbar
INTERNAL_IPS = [
    '127.0.0.1',  # Localhost
    '::1',        # IPv6 for localhost
]

# Logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    # Formatters define how logs are structured
    'formatters': {
        'verbose': {
            'format': '[{levelname}] {asctime} {name} - {message}',
            'style': '{',
        },
        'simple': {
            'format': '[{levelname}] {message}',
            'style': '{',
        },
    },

    # Handlers define where logs go
    'handlers': {
        'file': {
            'level': 'WARNING',  # WARNING, ERROR, CRITICAL
            'class': 'logging.FileHandler',
            'filename': BASE_DIR/ 'logs/django.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',  # Logs INFO and above to the console (Railway logs)
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },

    # Loggers define which parts of Django log what
    'loggers': {
        '': {
            'handlers': ['console', 'file'],
            'level': 'INFO', 
            'propagate': True,
        }
    }
}

#Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# For email verification of new accounts

def email_verified_callback(user):
    user.is_active = True


# def password_change_callback(user, password):
#     user.set_password(password)


# Global Package Settings
EMAIL_FROM_ADDRESS = 'angelina.chigrinetc.dev@gmail.com'  
EMAIL_PAGE_DOMAIN = 'http://127.0.0.1:8000/'  # mandatory (unless you use a custom link)
EMAIL_MULTI_USER = False  # optional (defaults to False)

# Email Verification Settings (mandatory for email sending)
EMAIL_MAIL_SUBJECT = 'ReFRESH: Please confirm your email'
EMAIL_MAIL_HTML = 'account/email/mail_body.html'
EMAIL_MAIL_PLAIN = 'account/email/mail_body.txt'
EMAIL_MAIL_TOKEN_LIFE = 60 * 60  # one hour

# Email Verification Settings (mandatory for builtin view)
EMAIL_MAIL_PAGE_TEMPLATE = 'account/email/email_success_template.html'
EMAIL_MAIL_CALLBACK = email_verified_callback

# Password Recovery Settings (mandatory for email sending)
# EMAIL_PASSWORD_SUBJECT = 'Change your password {{ user.username }}'
# EMAIL_PASSWORD_HTML = 'password_body.html'
# EMAIL_PASSWORD_PLAIN = 'password_body.txt'
# EMAIL_PASSWORD_TOKEN_LIFE = 60 * 10  # 10 minutes

# Password Recovery Settings (mandatory for builtin view)
# EMAIL_PASSWORD_PAGE_TEMPLATE = 'password_changed_template.html'
# EMAIL_PASSWORD_CHANGE_PAGE_TEMPLATE = 'password_change_template.html'
# EMAIL_PASSWORD_CALLBACK = password_change_callback


# For Django Email Backend
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'm #get emails by email
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'angelina.chigrinetc.dev@gmail.com'
EMAIL_HOST_PASSWORD = os.environ('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True

# stripe settings
STRIPE_PUBLISHABLE_KEY = os.environ('STRIPE_PUBLISHABLE_KEY')
STRIPE_SECRET_KEY = os.environ('STRIPE_SECRET_KEY')
STRIPE_WEBHOOK_SECRET = os.environ('STRIPE_WEBHOOK_SECRET')
STRIPE_API_VERSION = '2024-12-18.acacia'

# Celery
CELERY_BROKER_URL = os.environ('CELERY_BROKER_URL', default='redis://localhost:6379')
CELERY_RESULT_BACKEND = os.environ('CELERY_RESULT_BACKEND')
CELERY_RESULT_EXTENDED = True
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers.DatabaseScheduler'
# REST_FRAMEWORK

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    "DEFAULT_PERMISSION_CLASSES": [
        "api.permissions.IsAdminOrReadOnly", #custom
    ],
    "DEFAULT_PAGINATION_CLASS": "api.pagination.StandardResultsSetPagination", #custom
    "PAGE_SIZE": 15,
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

DJOSER = {
    "LOGIN_FIELD": "email",
    "SERIALIZERS": {
        "user_create": "api.serializers.CustomUserCreateSerializer",
    },
    'AUTH_HEADER_TYPES': ('JWT',),

}

# Additional security for production
CSRF_COOKIE_SECURE = os.environ('CSRF_COOKIE_SECURE') # ensures CSRF cookie is sent over HTTPS only
SESSION_COOKIE_SECURE = os.environ('SESSION_COOKIE_SECURE')  # ensures session cookies are only sent over HTTPS