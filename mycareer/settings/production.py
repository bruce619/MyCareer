from mycareer.settings.base import *
import dj_database_url
import django_heroku

# overwrite base.py settings here

DEBUG = config('DEBUG', cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

SECRET_KEY = config('SECRET_KEY')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', cast=int),
    }
}


# AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", '')
# AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", '')
# AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME", '')
# AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', '')
# S3_USE_SIGV4 = os.environ.get('S3_USE_SIGV4')

EMAIL_BACKEND = config('EMAIL_BACKEND')
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = "CAREERS AT NUE OFFSHORE <{}>".format(EMAIL_HOST_USER)
SERVER_EMAIL = EMAIL_HOST_USER


AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME')
S3_USE_SIGV4 = config('S3_USE_SIGV4')

AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_LOCATION = 'static'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

DEFAULT_FILE_STORAGE = 'mycareer.storage_backends.MediaStorage'

AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)


django_heroku.settings(locals())
