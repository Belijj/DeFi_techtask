@echo off

REM Запуск RabbitMQ
cd rabbitmq
docker-compose up -d

REM Переход в директорию microservices
cd ..\microservices

REM Активация виртуального окружения
call venv\Scripts\activate

REM Запуск data-generator.py в фоне
start python data-generator.py

REM Запуск socket-service.py
start uvicorn socket-service:app --host 0.0.0.0 --port 8001

REM Переход в директорию client
cd ..\client

REM Запуск клиентского приложения
npm start
