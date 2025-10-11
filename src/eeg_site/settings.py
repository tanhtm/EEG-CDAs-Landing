from whiteneuron.base.settings import _, environ
from whiteneuron.base.settings import *
from dotenv import load_dotenv
load_dotenv()

DATA_UPLOAD_MAX_NUMBER_FILES = environ.get("DATA_UPLOAD_MAX_NUMBER_FILES", 1000)

TINYMCE_KEY= environ.get("TINYMCE_KEY", "")

PROJECT_NAME = environ.get("PROJECT_NAME", "eeg_site")
NAME= environ.get("NAME", "White Neuron EEG Portal")
URL= environ.get("URL", f"https://portal.whiteneuron.com")

######################################################################
# Email
######################################################################
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = environ.get("EMAIL_HOST_USER", "anhnt@whiteneurons.com")
EMAIL_HOST_PASSWORD = environ.get("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = True

######################################################################
# General
######################################################################
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = environ.get("SECRET_KEY", get_random_secret_key())
# SECRET_KEY = "django-insecure-secret-key"

DEBUG = environ.get("DEBUG", "False") == "True"
# DEBUG = False

ROOT_URLCONF = f"{PROJECT_NAME}.urls"

BROWSER_RELOAD = environ.get("BROWSER_RELOAD", "False") == "True"
# BROWSER_RELOAD= False

# USE_CACHE = environ.get("USE_CACHE", "False") == "True"
USE_CACHE = False

WSGI_APPLICATION = f"{PROJECT_NAME}.wsgi.application"

######################################################################
# Domains
######################################################################
ALLOWED_HOSTS = environ.get("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
ALLOWED_HOSTS += ['localhost', '127.0.0.1', 'portal.whiteneuron.com']

CSRF_TRUSTED_ORIGINS = environ.get(
    "CSRF_TRUSTED_ORIGINS", "http://localhost:8000"
).split(",")
CSRF_TRUSTED_ORIGINS += [
    'https://portal.whiteneuron.com',
]

INSTALLED_APPS += [
    "apps.sites",
]

if DEBUG:
    if "debug_toolbar" not in INSTALLED_APPS:
        INSTALLED_APPS += ["debug_toolbar"]
else:
    try:
        INSTALLED_APPS.remove("debug_toolbar")
    except ValueError:
        pass

if BROWSER_RELOAD:
    if "django_browser_reload.middleware.BrowserReloadMiddleware" not in MIDDLEWARE:
        MIDDLEWARE.append("django_browser_reload.middleware.BrowserReloadMiddleware")
else:
    try:
        MIDDLEWARE.remove("django_browser_reload.middleware.BrowserReloadMiddleware")
    except ValueError:
        pass

if USE_CACHE:
    CACHENAME = environ.get("CACHENAME", "default")
    if CACHENAME == "default":
        CACHES= {'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        }}
    elif CACHENAME == "redis":
        CACHES= {"default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": environ.get("CACHE_REDIS_LOCATION", None),
        }}
        if not CACHES["default"]["LOCATION"]:
            print("CACHE_REDIS_LOCATION not set")
            sys.exit(1)
    else:
        print("Unknown cache backend")
        sys.exit(1)
    MIDDLEWARE = ["django.middleware.cache.UpdateCacheMiddleware"] + MIDDLEWARE + ["django.middleware.cache.FetchFromCacheMiddleware"]

if DEBUG:
    if "debug_toolbar.middleware.DebugToolbarMiddleware" not in MIDDLEWARE:
        MIDDLEWARE= ["debug_toolbar.middleware.DebugToolbarMiddleware"] + MIDDLEWARE
        INTERNAL_IPS = ["127.0.0.1"]
else:
    try:
        MIDDLEWARE.remove("debug_toolbar.middleware.DebugToolbarMiddleware")
    except ValueError:
        pass

######################################################################
# Templates
######################################################################
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [Path.joinpath(BASE_DIR, 'templates')],
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

######################################################################
# Languages
######################################################################

LANGUAGE_CODE = 'vi'

LANGUAGES = [
    ('vi', _('Vietnamese')),
    ('en', _('English')),
]

######################################################################
# Databases
######################################################################
DATABASE= environ.get("DATABASE", "sqlite")
DBROOT= BASE_DIR
if DATABASE == "sqlite":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": DBROOT / "db.sqlite3",
        },
    }
elif DATABASE == "postgres":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": environ.get("DATABASE_NAME"),
            "USER": environ.get("DATABASE_USER"),
            "PASSWORD": environ.get("DATABASE_PASSWORD"),
            "HOST": environ.get("DATABASE_HOST"),
            "PORT": environ.get("DATABASE_PORT"),
        }
    }

######################################################################
# Static
######################################################################
STATIC_URL = "static/"

import whiteneuron
WHITENEURON_PATH = Path(whiteneuron.__file__).parent
STATICFILES_DIRS = [
    BASE_DIR / "static",
    WHITENEURON_PATH / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_ROOT = DBROOT / "media"

MEDIA_URL = "/media/"

if DEBUG:
    STORAGES["staticfiles"]["BACKEND"] = "django.contrib.staticfiles.storage.StaticFilesStorage"
else:
    STORAGES["staticfiles"]["BACKEND"] =  "whitenoise.storage.CompressedStaticFilesStorage"

######################################################################
# Unfold
######################################################################
UNFOLD['SITE_HEADER'] = _(NAME)
UNFOLD['SITE_TITLE'] = _(NAME)
UNFOLD['ENVIRONMENT'] = f"{PROJECT_NAME}.utils.environment_callback"
UNFOLD['STYLES']= [lambda request: static("css/styles.css")] + UNFOLD['STYLES']
UNFOLD['SHOW_LANGUAGES'] = True
tool_items= []
navigations=[

    # {
    #     "title": _("Quản lý khách truy cập"),
    #     # "collapsible": True,
    #     "items": [
    #         {
    #             "title": "IP",
    #             "icon": "public",
    #             "link": reverse_lazy("admin:clients_ip_changelist"),
    #         },
    #         {
    #             "title": "Khách",
    #             "icon": "devices",
    #             "link": reverse_lazy("admin:clients_client_changelist"),
    #         },
    #         {
    #             "title": "Nhật ký hoạt động",
    #             "icon": "history",
    #             "link": reverse_lazy("admin:clients_log_changelist"),
    #         },
    #     ],
    # },
]
UNFOLD['SIDEBAR']['navigation']= UNFOLD['SIDEBAR']['navigation'][:1] + navigations + UNFOLD['SIDEBAR']['navigation'][1:]
UNFOLD["TABS"]= []
######################################################################
# Sentry
######################################################################
SENTRY_DSN = environ.get("SENTRY_DSN")

if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        enable_tracing=False,
    )

######################################################################
# Celery
######################################################################
CELERY_BROKER_URL = environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND= CELERY_BROKER_URL
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
########################################################################
# Timezone
########################################################################
TIME_ZONE = environ.get("TIME_ZONE", "Asia/Ho_Chi_Minh")
USE_TZ = True

########################################################################
# Session Configuration
########################################################################
# Use cache-based sessions to avoid file locking issues
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'
# Set session timeout - kéo dài để hạn chế phải đăng nhập lại khi dev
SESSION_COOKIE_AGE = 60 * 60 * 24 * 14  # 14 ngày
# Gia hạn mỗi request để duy trì phiên hoạt động
SESSION_SAVE_EVERY_REQUEST = True
# Không hết hạn khi đóng trình duyệt
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
CSRF_COOKIE_AGE = 60 * 60 * 24 * 30  # 30 ngày


SITE_ID = 1