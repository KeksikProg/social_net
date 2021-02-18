"""
Django settings for social_net project.

Generated by 'django-admin startproject' using Django 3.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('secret_key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'main',

    'easy_thumbnails',
    'django_cleanup',
    'bootstrap4',
    'crispy_forms',
    'social_django',
    'django_filters',
    'djoser',
    'rest_framework_social_oauth2',
    'oauth2_provider',

    'rest_framework',
    'rest_framework.authtoken'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'social_net.urls'

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
                'social_django.context_processors.backends',  # это и одно ниже для регистрации через соц сети
                'social_django.context_processors.login_redirect',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',  # Обычные токены, которые будут созранятся в базу данных
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # для жвт токенов
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',  # для авторизации с помощью OAUTH2
        'rest_framework_social_oauth2.authentication.SocialAuthentication',  # тоже самое для чего и выше
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend'  # Для фильтрации запросов drf
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',  # Что будет отвечать за пагинацию на сайте
    'PAGE_SIZE': 5,  # Какое кол-во записей будет выводится на 1 странице
}

DJOSER = {
    """
    Токен для авторизации передается в headers
    Заголовок в headers выглядит примерно так
    Authorization: Token <token>
    """

    'PASSWORD_RESET_CONFIRM_URL': '#/password/reset/confirm/{uid}/{token}',  # Для подтверждения сброса пароля
    'USERNAME_RESET_CONFIRM_URL': '#/username/reset/confirm/{uid}/{token}',  # Для подтверждения сброса юзернейма
    'ACTIVATION_URL': '#/activate/{uid}/{token}',  # Ссылка с активацией
    'SEND_ACTIVATION_EMAIL': True,  # Отправлять ли ссылку активации на почту
    'SERIALIZERS': {},
}

# smtp
EMAIL_PORT = os.getenv('email_port')  # Порт через который будут отправляется письма
EMAIL_USE_TLS = True  # Использовать ли протокол шифрования TLS
EMAIL_HOST = os.getenv('email_host')  # Какой протокол SMTP использовать
EMAIL_HOST_USER = os.getenv('email_host_user')  # Почта с которой будут отправлятся все письма
EMAIL_HOST_PASSWORD = os.getenv('email_host_pass')  # Пароль от это почты

WSGI_APPLICATION = 'social_net.wsgi.application'
CRISPY_TEMPLATE_PACK = 'bootstrap4'


SOCIAL_AUTH_VK_OAUTH2_KEY = os.getenv('vk_key')  # Секретный ключ который берется из приложения вконтакте
SOCIAL_AUTH_VK_OAUTH2_SECRET = os.getenv('vk_secret')  # тоже ключ и тоже берется из приложения

SOCIAL_AUTH_VK_OAUTH2_SCOPE = ['email']  # Чтобы дополнительно запросить у пользователя почту

AUTHENTICATION_BACKENDS = (  # Список классов реализующий аутентефикацию и авторизацию
    'social_core.backends.vk.VKOAuth2',  # Это и ниже для авторизации с помощью вк
    'django.contrib.auth.backends.ModelBackend',)

THUMBNAIL_BASEDIR = 'thumbs'


THUMBNAIL_ALIASES = {
    '': {
        'default': {
            'size': (201, 201),
            'crop': 'scale',
        }
    }
}


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('db_name'),
        'USER': os.getenv('db_user'),
        'PASSWORD': os.getenv('db_pass'),
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

REDIS_HOST = '127.0.0.1'
REDIS_PORT = '6379'
CELERY_BROKER_URL = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'
CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_RESULT_BACKEND = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'
CELERY_RESULT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

MEDIA_ROOT = os.path.join(BASE_DIR, 'media') 
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = '/media/'
STATIC_URL = '/static/'