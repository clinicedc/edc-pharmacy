# http://cheng.logdown.com/posts/2015/01/29/deploy-django-nginx-gunicorn-on-mac-osx-part-2
# cd /home/django/source/edc-pharma/
# gunicorn -c gunicorn.conf.py edc-pharma.wsgi --pid /home/django/source/edc-pharma/logs/gunicorn.pid --daemon
#

import os

SOURCE_ROOT = os.path.expanduser('~/source')

bind = "127.0.0.1:9000"  # Don't use port 80 because nginx occupied it already.
errorlog = os.path.join(SOURCE_ROOT, 'edc-pharma/logs/gunicorn-error.log')  # Make sure you create the log folder
accesslog = os.path.join(SOURCE_ROOT, 'edc-pharma/logs/gunicorn-access.log')
loglevel = 'debug'
workers = 1  # the number of recommended workers is '2 * number of CPUs + 1'
