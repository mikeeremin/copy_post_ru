# -*- coding: utf-8 -*-
# Django settings for copypost project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

def requestToTemplates(request):
    return {'request': request}

def news(request):
    from news.models import News
    return {'news' : News.objects.all().order_by('-pdate')[:5]}

def faq(request):
    from faq.models import FaqAnswers
    return {'faqs' : FaqAnswers.objects.all()[:3]}

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    'settings.requestToTemplates',
    'settings.news',
    'settings.faq',
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.contrib.messages.context_processors.messages")

ADMINS = (
# ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'copypost', # Or path to database file if using sqlite3.
        'USER': 'copypost', # Not used with sqlite3.
        'PASSWORD': 'fQyv52XCwUhTcWmw', # Not used with sqlite3.
        'HOST': '', # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '', # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
# Put strings here, like "/home/html/static" or "C:/www/django/static".
# Always use forward slashes, even on Windows.
# Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
    )

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'k^5&rube4r2hf3m^9nvv$qg((-s7itv*vdmak+cwz+0*%8i+oo'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #     'django.template.loaders.eggs.Loader',
    )

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    )

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = ('templates',)

INSTALLED_APPS = (
    #'invitation',
    'registration',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'south',
    'my',
    'news',
    'faq'
    )

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
            },
        }
}

twitter_settings = {
    #ACCESS
    'CONSUMER_KEY': "MAgq5kl5FF151Z3CdE6kEA",
    'CONSUMER_SECRET': "EcgX71Jj0hUPCLPDvGSPS43rstGU4UAOWX2Z5IVM",

    #TWITTER URLS
    'REQUEST_TOKEN_URL': 'https://api.twitter.com/oauth/request_token',
    'ACCESS_TOKEN_URL': 'https://api.twitter.com/oauth/access_token',
    'AUTHORIZATION_URL': 'https://api.twitter.com/oauth/authorize',
    'SIGNIN_URL': 'https://api.twitter.com/oauth/authenticate',
    }

ACCOUNT_ACTIVATION_DAYS = 2
AUTH_USER_EMAIL_UNIQUE = True
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = 'noreply@seopass.ru'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

HTTP_HOST = "http://copy-post.ru"

fb_settings = {
    "client_id": "119375981504441",
    "client_secret": "70f871d1c3d498088350c7b38dbf8114",
    "redirect_uri": "%s" % HTTP_HOST,
    "permission": "publish_stream,offline_access,user_groups,friends_groups",
    "post_from": "copy-post.ru"
}

vk_settings = {
    'VKONTAKTE_CLIENT_ID': "2663418",
    'VKONTAKTE_CLIENT_SECRET': "g7UEx5hIAub6inwlhgQ8",
    }

fs_settings = {
    'clientid' :'TIINZSMUJFLCRWFU2RL1GPLBJRQI1HQUFETKWOLNPQVBC21L',
    'clientsecret' : '1KSAPLD3H0BXECJT4K5WOOJL2WIP5EXE5AI5ITEZ0C0OMIH5'
}

SYNC_BIN = "sync.py"

AUTH_PROFILE_MODULE = 'my.UserProfile'