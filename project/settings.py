import os

import dj_database_url
from environs import Env

env = Env()
env.read_env()

DATABASE_URL = env("DATABASE_URL")

DATABASES = {'default': dj_database_url.config(f'DATABASE_URL', conn_max_age=None)}

INSTALLED_APPS = ['datacenter']

SECRET_KEY = env("SECRET_KEY")

DEBUG = env.bool("DEBUG", False)

ROOT_URLCONF = 'project.urls'

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", subcast=str)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
    },
]

USE_L10N = True

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
