FROM python:3.5

COPY requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt && rm /tmp/requirements.txt

ADD . /opt/bierklub
WORKDIR /opt/bierklub/bierklub

RUN chmod -R 777 /opt/bierklub/bierklub/klubevents/static

ENTRYPOINT env DJANGO_SETTINGS_MODULE=bierklub.settings gunicorn \
  -w 2 bierklub.wsgi:application -b 0.0.0.0:8000
