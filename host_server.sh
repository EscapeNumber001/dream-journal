#!/usr/bin/bash

source ./.venv/bin/activate
uwsgi --module=mysite.wsgi:application \
--env DJANGO_SETTINGS_MODULE=mysite.settings \
--master \
--pidfile=/tmp/project-master.pid \
--http=0.0.0.0:49152 \
--max-requests=5000 \
--processes=5 \
--static-map /static=hello/static/
