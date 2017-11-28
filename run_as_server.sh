python manage.py migrate
python manage.py makemigrations DjangoRESTImage
python manage.py migrate DjangoRESTImage
wsgi --ini /etc/uwsgi.ini &

