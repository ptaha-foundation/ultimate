#!/bin/sh

python manage.py create_periodic_task
python manage.py runserver 0.0.0.0:8000
