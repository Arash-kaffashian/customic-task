FROM python:3.11-slim

WORKDIR /app

# جلوگیری از بافر شدن خروجی‌ها
ENV PYTHONUNBUFFERED 1

# نصب وابستگی‌ها
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# پورت جنگو
EXPOSE 8000
