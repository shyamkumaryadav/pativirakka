from .base import *
import dj_database_url
import django_heroku

SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = False
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '[contactor] %(levelname)s %(asctime)s %(message)s'
        },
    },
    'handlers': {
        # Send all messages to console
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        # Send info messages to syslog
        # 'syslog':{
        #     'level':'INFO',
        #     'class': 'logging.handlers.SysLogHandler',
        #     'facility': SysLogHandler.LOG_LOCAL2,
        #     'address': '/dev/log',
        #     'formatter': 'verbose',
        # },
        # Warning messages are sent to admin emails
        # 'mail_admins': {
        #     'level': 'WARNING',
        #     'filters': ['require_debug_false'],
        #     'class': 'django.utils.log.AdminEmailHandler',
        # },
        # critical errors are logged to sentry
        'sentry': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'raven.contrib.django.handlers.SentryHandler',
        },
    },
    'loggers': {
        # This is the "catch all" logger
        '': {
            'handlers': ['console', 'syslog', 'mail_admins', 'sentry'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}

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
