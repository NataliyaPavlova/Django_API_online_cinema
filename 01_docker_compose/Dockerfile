FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/

RUN apt-get update --yes --quiet && \
    apt-get install --yes --quiet --no-install-recommends \
                    libpq-dev python-dev libjpeg62-turbo-dev zlib1g-dev && \
    /usr/local/bin/python -m pip install --upgrade pip && \
    pip install -r /app/requirements.txt &&\
    mkdir media && mkdir static

COPY . /app

EXPOSE 8000

CMD ["gunicorn","--bind","0.0.0.0:8000","config.wsgi:application"]

