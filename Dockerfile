FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 8000

ENV DATABASE_URL=postgresql://admin:admin@postgres:5432/database

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
