# Dockerfile - this is a comment. Delete me if you want.
FROM python:3.8-alpine3.10
COPY . /BloombergLineBot
WORKDIR /BloombergLineBot
RUN apk add --no-cache --virtual .build-deps musl-dev gcc linux-headers && pip install -r requirements.txt && apk del .build-deps musl-dev gcc
RUN adduser -r flask
USER flask

EXPOSE 5000
CMD ["uwsgi", "--http-socket", "0.0.0.0:5000", "--wsgi-file", "Server.py", "--callable", "server"]
