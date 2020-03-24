# Dockerfile - this is a comment. Delete me if you want.
FROM python:3.8-alpine3.10
COPY . /BloombergLineBot
WORKDIR /BloombergLineBot
RUN apk add --no-cache --virtual .build-deps gcc musl-dev
RUN pip install cython
RUN apk del .build-deps gcc musl-dev
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["Server.py"]