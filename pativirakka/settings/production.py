from .base import *
import dj_database_url
import django_heroku

SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = False

ALLOWED_HOSTS = [".ngrok.io", ".herokuapps.com"]

INSTALLED_APPS += ["whitenoise.runserver_nostatic", ]

MIDDLEWARE += ['whitenoise.middleware.WhiteNoiseMiddleware', ]

DATABASES['default'] = dj_database_url.config(
    conn_max_age=600, ssl_require=True)

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Django Storage Dropbox (User Videos and Images)
# https://django-storages.readthedocs.io/en/latest/backends/dropbox.html

DROPBOX_OAUTH2_TOKEN = os.getenv('DROPBOX_OAUTH2_TOKEN')
DEFAULT_FILE_STORAGE = 'storages.backends.dropbox.DropBoxStorage'
django_heroku.settings(locals())
