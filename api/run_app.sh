#!/bin/sh

gunicorn -w 3 -b :5000 -t 30 --reload api.wsgi:app
