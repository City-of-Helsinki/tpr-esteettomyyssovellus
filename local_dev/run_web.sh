#!/bin/sh

# run Django development server

# wait for PSQL server to start
sleep 20

python manage.py migrate --database=ar_db

python manage.py runserver 0.0.0.0:8000
