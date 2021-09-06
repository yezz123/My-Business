FROM python:3.9.2


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


WORKDIR /app

COPY . /app


RUN pip install -r requirements.txt


ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["python3","gunicorn","common.wsgi","--bind=0.0.0.0:8000"]
