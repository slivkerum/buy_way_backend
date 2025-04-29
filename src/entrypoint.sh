#!/bin/sh
#/usr/local/bin/python manage.py collectstatic --noinput
/opt/venv/bin/uwsgi --ini uwsgi.ini
