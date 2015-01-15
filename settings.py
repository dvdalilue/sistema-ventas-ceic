# Django settings for SistemaCaja project.

from os import path

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Oliver', 'oliver.a.perez.c@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', 
        'NAME': 'sistemaventas',                           
        'USER': 'ceic',
        'PASSWORD': 'cu4rt1c0s3gur0',
        'HOST': 'localhost',                      
        'PORT': '5432',                      
    }
}


TIME_ZONE = 'America/Caracas'
LANGUAGE_CODE = 'es-ve'

SITE_ID = 1

USE_I18N = True
USE_L10N = True


PROJECT_ROOT = path.dirname(path.abspath(__file__))

MEDIA_ROOT = PROJECT_ROOT + '/media/'
MEDIA_URL = '/media/'

STATIC_ROOT = '/home/max/SistemaCaja/static/'
STATIC_URL = '/static/'

ADMIN_MEDIA_PREFIX = '/static/admin/'

STATICFILES_DIRS = (
    ('site', PROJECT_ROOT+'/site-static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'bhj++&et^6nuw)!-l%5p3s*-!1e4=w4ce1b(g698m_q5o1xxp6'

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

ROOT_URLCONF = 'sistema-ventas-ceic.urls'

TEMPLATE_DIRS = (
    PROJECT_ROOT+'/Templates',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    #'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ventas_app',
    'django.contrib.admin',
    # 'django.contrib.admindocs',
)

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

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
