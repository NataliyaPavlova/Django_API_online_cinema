FROM python:3.8-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r /app/requirements.txt

COPY . /app

EXPOSE 8000

CMD ["gunicorn","--bind","0.0.0.0:8000","config.wsgi:application"]

