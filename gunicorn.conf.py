import os

SOURCE_ROOT = os.path.expanduser('~/source')

bind = "127.0.0.1:9000"  # Don't use port 80 because nginx occupied it already.
# Make sure you create the log folder
errorlog = os.path.join(SOURCE_ROOT, 'edc-pharmacy/logs/gunicorn-error.log')
accesslog = os.path.join(SOURCE_ROOT, 'edc-pharmacy/logs/gunicorn-access.log')
loglevel = 'debug'
workers = 1  # the number of recommended workers is '2 * number of CPUs + 1'
