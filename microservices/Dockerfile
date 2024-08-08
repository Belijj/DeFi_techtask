# Используйте официальный Python-образ
FROM python:3.12-slim

# Установите рабочую директорию
WORKDIR /app

# Скопируйте файл зависимостей
COPY requirements.txt .

# Установите зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Скопируйте все файлы из директории
COPY . .

# Запустите нужный скрипт
CMD ["python", "data-generator.py"]
