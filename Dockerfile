# Dockerfile - this is a comment. Delete me if you want.
FROM python:3.8-alpine3.10
COPY . /BloombergLineBot
WORKDIR /BloombergLineBot
RUN apk add --no-cache --virtual .build-deps gcc musl-dev libressl-dev libffi-dev \
    && apk add gcc musl-dev python3-dev \
    && pip install cython \
    && pip install -r requirements.txt \
    ENTRYPOINT ["python3"]
CMD ["Server.py"]