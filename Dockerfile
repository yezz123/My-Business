FROM alpine:3.7

WORKDIR /app

COPY requirements.txt /app/requirements.txt
COPY accounts /app/accounts
COPY common /app/common
COPY invoices /app/invoices
COPY partners /app/partners
COPY projects /app/projects
COPY servers /app/servers
COPY manage.py /app
COPY config.ini.defaults /app/config.ini.defaults
COPY example_template.pdf /app/example_template.pdf

RUN \
    apk add --no-cache python3 postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc python3-dev musl-dev postgresql-dev && \
    python3 -m pip install -r requirements.txt --no-cache-dir && \
    apk --purge del .build-deps

EXPOSE 8000

CMD ["python3","gunicorn","common.wsgi","--bind=0.0.0.0:8000"]
