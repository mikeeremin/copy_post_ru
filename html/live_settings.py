# -*- coding: utf-8 -*-

from settings import *

DEBUG = True
TEMPLATE_DEBUG = True

ADMINS = (
    ('Mike Eremin', 'meremin@gmail.com'),
    )

#CACHE_BACKEND = 'memcached://127.0.0.1:11211/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'copypost', # Or path to database file if using sqlite3.
        'USER': 'copypost', # Not used with sqlite3.
        'PASSWORD': 'fQyv52XCwUhTcWmw', # Not used with sqlite3.
        'HOST': 'mysql1', # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '', # Set to empty string for default. Not used with sqlite3.
    }
}

TEMPLATE_DIRS = ('/var/www/html/dev.copy-post.ru/html/templates',)
ADMIN_MEDIA_PREFIX = '/admin_media/'
HTTP_HOST = "http://dev.copy-post.ru"
SYNC_BIN = "/var/www/html/dev.copy-post.ru/html/sync.sh"

fb_settings = {
    "client_id": "119375981504441",
    "client_secret": "70f871d1c3d498088350c7b38dbf8114",
    "redirect_uri": "%s" % HTTP_HOST,
    "permission": "publish_stream,offline_access,user_groups,friends_groups",
    "post_from": "dev.copy-post.ru"
}

