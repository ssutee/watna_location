# Django settings for watna_location project.

import os.path, os, sys

sys.path.append(os.path.abspath(sys.path[0]+'/..'))

GMAPI_MAPS_URL = "https://maps.googleapis.com/maps/api/js?key=AIzaSyAsPczcWkcD5o1TLY22ViG_QvMPkWYMsPk&sensor=false"

CRISPY_TEMPLATE_PACK = 'bootstrap'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Sutee Sudprasert', 'sutee.s@gmail.com'),
)

ugettext = lambda s: s

LANGUAGES = (
  ('th', ugettext('Thai')),
  ('en', ugettext('English')),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'watna_location',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': 'g2-94b',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Asia/Bangkok'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'th'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

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
STATIC_ROOT = '/home/sutee/watna_location/static/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    ('css', '/home/sutee/watna_location/css'),
    ('media', '/home/sutee/watna_location/media'),
    ('gmapi', '/home/sutee/watna_location/gmapi'),  
    ('bootstrap', '/home/sutee/watna_location/bootstrap'),
    ('waypoints', '/home/sutee/watna_location/waypoints'),
    ('flexi', '/home/sutee/watna_location/flexi'),
    ('jscolor', '/home/sutee/watna_location/jscolor'),    
)

LOCALE_PATHS = (
    '/home/sutee/watna_location/locale',
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '5%52*rb2n8w#s^r5vml-b()@%kf49u-1f67r7s3lp#2_gyq-=l'

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
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'djangoflash.middleware.FlashMiddleware',    
    'django.middleware.locale.LocaleMiddleware',    
)

ROOT_URLCONF = 'watna_location.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'watna_location.wsgi.application'

TEMPLATE_DIRS = (
    '/home/sutee/watna_location/templates'
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django_countries',
    'crispy_forms',
    'location',
    'gmapi',
    'south',
    'jquery',
    'emailusernames',
)

AUTHENTICATION_BACKENDS = (
    'emailusernames.backends.EmailAuthBackend',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
    'djangoflash.context_processors.flash',
    'django.core.context_processors.i18n',
    'location.context_processors.map_type',
)



# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
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

try:
    from local_settings import *
except ImportError, e:
    pass