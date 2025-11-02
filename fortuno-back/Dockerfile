FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

# Run migrations and start gunicorn
CMD sh -c "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn fortuno.wsgi:application --bind 0.0.0.0:${PORT:-8000}"