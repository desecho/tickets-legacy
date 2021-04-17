FROM python:2.7-alpine

ADD requirements.txt /app/requirements.txt

RUN apk add --no-cache --virtual .build-deps gcc musl-dev libffi-dev openssl-dev python2-dev cargo && \
    apk add --no-cache mariadb-dev jpeg-dev && \
    pip install --no-cache-dir -r /app/requirements.txt && \
    apk del .build-deps

ADD tickets_project /app
WORKDIR /app
ARG SECRET_KEY=key

RUN ./manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "tickets_project.wsgi:application"]
