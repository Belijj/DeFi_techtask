# Application Workflow and Launch Instructions

## Workflow Overview

1. **Data Generator**:
   - Simulates traffic by generating messages every 5 seconds.
   - Sends generated messages to a RabbitMQ queue.

2. **Socket Service**:
   - Consumes messages from the RabbitMQ queue.
   - Returns messages via the `/ws` endpoint.
   - Capable of receiving data from the client, sending it back to the RabbitMQ queue.

3. **Client**:
   - Displays messages from the data queue.
   - Provides functionality to send messages to the queue.

## Application Launch Steps

### 1. RabbitMQ Setup

1. Navigate to the RabbitMQ directory:
   ```bash
      cd ./rabbitmq
      docker-compose up(wait for instalation)
### 2. Microservices Launch
   ```bash
      cd ./microservices
      2.1 ./venv/scripts/Activate
      2.2 python data-generator.py
      2.3 uvicorn socket-service:app --host 0.0.0.0, --port 8001
### 3. FrontEnd Launch
   ```bash
       3. cd ./client
       3.1 nmp install
       3.2 serve-s build

### 4. Tests
   ```bash
       4.1 Webscoket+ rabbitMQ test
           4.2 Launch RabbitMQ and activate the virtual environment (venv)if it has not been activated previously.
           4.3 cd ./docs
           4.4 pytest -v
       4.5 Client test
           4.6 cd ./client
           4.7 npm test
