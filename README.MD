# WebSocket Server with RabbitMQ and FastAPI

## Overview

### This project sets up a WebSocket server using FastAPI that handles real-time communication between clients. It integrates with RabbitMQ for message queuing and persistence. The server also interacts with an SQLite database to store and retrieve chat messages.

### Features
- Real-time communication: Supports multiple WebSocket clients for live messaging.
- Message persistence: Stores and retrieves chat messages using Postgre.
- Message broadcasting: Distributes messages to all connected clients.
- RabbitMQ integration: Publishes and listens to messages from RabbitMQ.
- Retrieving messages: Once a new client is connected to chat, server retrieves 5 last messages from the chat.

### Workflow

# Client Connection

- Client Connection: Clients connect to the WebSocket server by providing a unique client_id. Once connected, they receive the latest chat messages and can start sending new messages.

# Message Handling

- Message Handling: Messages received from clients are stored in the PostgreSQL database and broadcasted to Rabbit queue.

# RabbitMQ Integration
- The server listens for incoming messages from RabbitMQ and broadcasts them to all connected clients. It also publishes       messages to RabbitMQ for external consumption or further processing.

### Application Launch
1. **RabbitMQ Setup**
   - cd ./backend
   - cd ./rabbitmq
   - docker-compose up

2. **Server Launch**
   - cd ./backend
   - ./venv/scripts/Activate
   - uvicorn main:app --host 0.0.0.0 --port 8080
   - (I assume postgre is running at localhost:5432)

3. **Frontend Launch**
   - cd ./client
   - npm install
   - serve -s build

4. **Tests**
   - **WebSocket + RabbitMQ Test**
     - (Make sure that RabbitMQ is running and venv is active).
     - cd ./backend
     - pytest -v
# Test simulates 1000 users actively commincating in the chat, sending 100 messages per second. On my local machine(16gb ram, I3 10100) test works fine.
