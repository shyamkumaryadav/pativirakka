from ckeditor.configs import DEFAULT_CONFIG
import os

BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))

SECRET_KEY = "09j#soyd6se9jwf_!m!y*4jhks_l1_(r-8se5bvuw#)$%i8l6@"


DEBUG = True


ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "ckeditor",
    "pativirakka",
    "django_cleanup",
    "crispy_forms",
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "pativirakka.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "pativirakka.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator", },
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator", },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"

LANGUAGE_COOKIE_NAME = "pativirakka_LANGUAGE"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Email

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]


# media files (Image, Video)
MEDIA_URL = "/media/"


LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'


AUTH_USER_MODEL = 'pativirakka.User'


CUSTOM_TOOLBAR = [
    {
        "name": "document",
        "items": [
            "Styles", "Format", "Maximize", "Preview", "Blockquote", "Bold", "Italic", "Underline", "Strike", " -",
            "TextColor", "BGColor",  "-",
            "JustifyLeft", "JustifyCenter", "JustifyRight", "JustifyBlock",
        ],
    },
    {
        "name": "widgets",
                "items": [
                    "Undo", "Redo", "-",
                    "NumberedList", "BulletedList", "-",
                    "Outdent", "Indent", "-",
                    "Link", "Unlink", "-",
                    "Image", "CodeSnippet", "Table", "HorizontalRule", "SpecialChar", "-",
                ],
    },
]

CKEDITOR_CONFIGS = {
    "default": DEFAULT_CONFIG,
    "my-custom-toolbar": {
        "skin": "moono-lisa",
        "toolbar": CUSTOM_TOOLBAR,
        'height': "auto",
        'width': "auto",
        "toolbarGroups": None,
        "extraPlugins": ",".join(["image2", "codesnippet", "preview"]),
        "removePlugins": ",".join(["image", "smiley"]),
        "codeSnippet_theme": "xcode",
    },
}
