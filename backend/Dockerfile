FROM python:3.9.6-slim-buster
WORKDIR /app
COPY . .
RUN apt-get update \
	&& apt-get -y install libpq-dev gcc \
	&& pip install -r requirements.txt
ENTRYPOINT python manage.py makemigrations \
	&& python manage.py migrate \
	# && python manage.py collectstatic --noinput --clear\
	&& (python manage.py createsuperuser --noinput \
	&& python manage.py initialize_tables || true) \
	&& gunicorn unicoding.wsgi:application -w 4 --bind 0.0.0.0:8000