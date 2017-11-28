python manage.py migrate
python manage.py makemigrations DjangoRESTImage
python manage.py migrate DjangoRESTImage
uwsgi --ini /etc/uwsgi.ini &

