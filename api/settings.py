"""
Django settings for api project.

Generated by 'django-admin startproject' using Django 4.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import environ
import os
import datetime
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
APP_VERSION = "1.0"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Setup environment variables.
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = [
    '*'
]

CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = (
    'localhost:3000',
    '127.0.0.1:3000',
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'https://localhost:3000',
    'https://127.0.0.1:3000'
)
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
]
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'tests',
    'users',
    'degree_types',
    'certificate_types',
    'day_off_types',
    'employment_contract_types',
    'addresses',
    'ethnicities',
    'religions',
    'nationalities',
    'positions',
    'companies',
    'kinds_of_work',
    'literacy',
    'customers',
    'projects',
    'notification',
    'branchs',
    'departments',
    'staffs',
    'promotions',
    'skills',
    'urgent_contacts',
    'bonuses',
    'health_status',
    'day_off_years',
    'day_off_year_details',
    'certificate',
    'degree',
    'discipline',
    'salaries',
    'timekeeping',
    'staff_project',
    'employment_contracts',
    'up_salaries',
    'recruitment_requirements',
    'recruitment_requirement_details',
    'recruitment_tracking',
    'trainning_requirement',
    'trainning_requirement_detail',
    'dashboard',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',

]

ROOT_URLCONF = 'api.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'api.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
        'OPTIONS': {
            'client_encoding': 'UTF-8'  # Need to set when create new database
        },
    },
}

AUTH_USER_MODEL = 'users.User'

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),

    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),

    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 'rest_framework.authentication.BasicAuthentication',
        # 'rest_framework.authentication.TokenAuthentication',
        # 'rest_framework_simplejwt.authentication.JWTAuthentication',
        'django_cognito_jwt.JSONWebTokenAuthentication'
    ],
    
    # Pagination
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'PAGINATE_BY_PARAM': 'page_size',
    
    'EXCEPTION_HANDLER': 'base.utils.custom_exception_handler',
}
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=3600),
    'JWT_ALLOW_REFRESH': True
}


# S3 SETTINGS (for upload media)
S3_ACCESS_KEY = env('S3_ACCESS_KEY')
S3_SECRET_KEY = env('S3_SECRET_KEY')
S3_REGION = env('S3_REGION')
S3_BUCKET_NAME = env('S3_BUCKET_NAME')
S3_URL = env('S3_URL')  # Using .cloudfront.net url for auto resize and adjust media

# COGNITO SETTINGS
COGNITO_AWS_REGION = env('COGNITO_AWS_REGION')
COGNITO_USER_POOL = env('COGNITO_USER_POOL')  # <user pool id>
COGNITO_AUDIENCE = env('COGNITO_AUDIENCE')  # <client id>
COGNITO_AUDIENCE_SECRET = env('COGNITO_AUDIENCE_SECRET')

# REDIS & CELERY SETTINGS
REDIS_HOST = env('REDIS_HOST')
REDIS_PASSWORD = env('REDIS_PASSWORD')
REDIS_PORT = env('REDIS_PORT')
REDIS_CHANNEL = env('REDIS_CHANNEL')
REDIS_CELERY_CHANNEL = env('REDIS_CELERY_CHANNEL')
CELERY_BROKER_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_CELERY_CHANNEL}"
CELERY_RESULT_BACKEND = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_CELERY_CHANNEL}"
CELERY_IMPORTS = (
    "base.tasks",
)

CELERY_ACCEPT_CONTENT = ['pickle']
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_RESULT_SERIALIZER = 'pickle'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = 'HRM <havanlinh19042000@gmail.com>'

# FIREBASE SETTINGS
FCM_SERVER_KEY = env('FCM_SERVER_KEY')

FRONTEND_URL = env('FRONTEND_URL')