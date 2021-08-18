FROM alpine:3.7

WORKDIR /app

COPY . /app


RUN \
    apk add --no-cache python3 postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc python3-dev musl-dev postgresql-dev && \
    python3 -m pip install -r requirements.txt --no-cache-dir && \
    apk --purge del .build-deps

EXPOSE 8000

CMD ["python3","gunicorn","common.wsgi","--bind=0.0.0.0:8000"]
