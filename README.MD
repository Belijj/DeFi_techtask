# This repository shows my knowledge of websockets and message brokers(RabbitMQ). There is also a chatbot capable of handling 1000 active users at "chatbot" branch.

# Application Workflow and Launch Instructions

## Workflow Overview

### Data Generator
- Simulates traffic by generating messages every 5 seconds.
- Sends generated messages to a RabbitMQ queue.

### Socket Service
- Consumes messages from the RabbitMQ queue.
- Returns messages via the `/ws` endpoint.
- Capable of receiving data from the client and sending it back to the RabbitMQ queue.

### Client
- Displays messages from the data queue.
- Provides functionality to send messages to the queue.

## Application Launch Steps

1. **RabbitMQ Setup**
   - 'cd ./rabbitmq`
   - docker-compose up

2. **Microservices Launch**
   - cd ./microservices
   - ./venv/scripts/Activate
   - python data-generator.py
   - uvicorn socket-service:app --host 0.0.0.0 --port 8001

3. **Frontend Launch**
   - cd ./client
   - npm install
   - serve -s build

4. **Tests**
   - **WebSocket + RabbitMQ Test**
     - (Make sure that RabbitMQ is running and venv is active).
     - cd ./docs
     - pytest -v
   - **Client Test**
     - cd ./client
     - npm test

---
