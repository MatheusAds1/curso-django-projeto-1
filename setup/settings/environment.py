from pathlib import Path
import os
from django.contrib.messages import constants
from utils.environment import get_env_variable, parse_comma_sep_str_to_list


BASE_DIR = Path(__file__).resolve().parent.parent.parent

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = os.environ.get('SECRET_KEY', 'INSECURE')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if os.environ.get('DEBUG') == '1' else False

ALLOWED_HOSTS: list[str] = parse_comma_sep_str_to_list(
    get_env_variable('ALLOWED_HOST')
)
CSRF_TRUSTED_ORIGINS: list[str] = parse_comma_sep_str_to_list(
    get_env_variable('CSRF_TRUSTED_ORIGINS')
)

ROOT_URLCONF = 'setup.urls'

WSGI_APPLICATION = 'setup.wsgi.application'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'