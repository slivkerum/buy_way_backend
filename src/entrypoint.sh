#!/bin/sh
python manage.py collectstatic --noinput
/opt/venv/bin/uwsgi --ini uwsgi.ini
