FROM python:3.8

WORKDIR /app
COPY requirements.txt /app/requirements.txt
COPY . .

RUN python -m venv env && \
    apt-get update --yes --quiet && \
    apt-get install --yes --quiet --no-install-recommends \
                    libpq-dev python-dev libjpeg62-turbo-dev zlib1g-dev && \
    env/bin/pip install --upgrade pip && \
    env/bin/pip install -r /app/requirements.txt &&\
    mkdir media && mkdir static

ENV PYTHONUNBUFFERED=1 \
    PORT=8000 \
    PATH='/app/env/bin:${PATH}'

EXPOSE 8000

CMD python manage.py makemigrations movies && \
    python manage.py migrate && \
    python manage.py collectstatic --no-input && \
    gunicorn -b 0.0.0.0:8000 --log-level=debug config.wsgi

