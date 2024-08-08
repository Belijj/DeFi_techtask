# Используйте официальный Node.js-образ
FROM node:16

# Установите рабочую директорию
WORKDIR /app

# Скопируйте package.json и установите зависимости
COPY package*.json ./
RUN npm install

# Скопируйте оставшийся код
COPY . .

# Откройте порт 3000
EXPOSE 3000

# Запуск клиентского приложения
CMD ["npm", "start"]
