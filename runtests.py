#!/usr/bin/env python
import django
import logging
import os
import sys

from django.conf import settings
from django.test.runner import DiscoverRunner
from os.path import abspath, dirname, join


class DisableMigrations:

    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None


base_dir = dirname(abspath(__file__))
app_name = 'edc_pharmacy'

installed_apps = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'simple_history',
    'django_revision.apps.AppConfig',
    'edc_appointment.apps.AppConfig',
    'edc_device.apps.AppConfig',
    'edc_identifier.apps.AppConfig',
    'edc_timepoint.apps.AppConfig',
    'edc_metadata.apps.AppConfig',
    'edc_metadata_rules.apps.AppConfig',
    'edc_pharmacy.apps.EdcLabelAppConfig',
    'edc_pharmacy.apps.EdcBaseAppConfig',
    'edc_pharmacy.apps.EdcFacilityAppConfig',
    'edc_pharmacy.apps.AppConfig', ]

DEFAULT_SETTINGS = dict(
    BASE_DIR=base_dir,
    SITE_ID=10,
    ALLOWED_HOSTS=['localhost'],
    # AUTH_USER_MODEL='custom_user.CustomUser',
    ROOT_URLCONF=f'{app_name}.urls',
    STATIC_URL='/static/',
    INSTALLED_APPS=installed_apps,
    DATABASES={
        # required for tests when acting as a server that deserializes
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': join(base_dir, 'db.sqlite3'),
        },
        'client': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': join(base_dir, 'db.sqlite3'),
        },
    },
    TEMPLATES=[{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ]
        },
    }],
    MIDDLEWARE=[
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ],

    LANGUAGE_CODE='en-us',
    TIME_ZONE='UTC',
    USE_I18N=True,
    USE_L10N=True,
    USE_TZ=True,

    APP_NAME=app_name,
    EDC_BOOTSTRAP=3,
    STATIC_ROOT=os.path.join(base_dir, app_name, 'static'),
    LABEL_PRINTER='test_label_printer_ambition',
    COUNTRY='botswana',
    HOLIDAY_FILE=os.path.join(base_dir, app_name, 'tests', 'holidays.csv'),
    DASHBOARD_URL_NAMES={
        'subject_listboard_url': 'edc_subject_dashboard:subject_listboard_url',
        'subject_dashboard_url': 'edc_subject_dashboard:subject_dashboard_url',
    },

    DEFAULT_FILE_STORAGE='inmemorystorage.InMemoryStorage',
    MIGRATION_MODULES=DisableMigrations(),
    PASSWORD_HASHERS=('django.contrib.auth.hashers.MD5PasswordHasher', ),
)


def main():
    if not settings.configured:
        settings.configure(**DEFAULT_SETTINGS)
    django.setup()
    failures = DiscoverRunner(failfast=True).run_tests(
        [f'{app_name}.tests'])
    sys.exit(failures)


if __name__ == "__main__":
    logging.basicConfig()
    main()
