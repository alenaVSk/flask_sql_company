FROM python:3.10-slim-buster

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
COPY dump_fcompany_pg.sql /app/dump_fcompany_pg.sql

EXPOSE 5000

#CMD ["gunicorn", "-b", "0.0.0.0:5000", "fcompany:app"]    - вернуть после деплоя на heroky

CMD ["gunicorn", "-b", "0.0.0.0:$PORT", "fcompany:app"]
