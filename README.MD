Workflow:

Data generator simulates traffic by generating messages every 5 sec, and sends them into rabbitMQ queue.
Socket-service consumes messages from rabbitMQ and returns them via /ws endpoint.
This endpoint is also capable of receiving data from client(data is sent to rabbitMQ queue).
Client part displays messages from data queue, and also provides functionality to send messages to the queue.






Application Launch:

1. cd ./rabbitmq 
    1.1 docker-compose up(wait for instalation)

2. cd ./microservices
    2.1 ./venv/scripts/Activate
    2.2 python data-generator.py
    2.3 uvicorn socket-service:app --host 0.0.0.0, --port 8001

3. cd ./client
    3.1 nmp install
    3.2 serve-s build

4. Tests:
    4.1 Webscoket+ rabbitMQ test
        4.2 Launch RabbitMQ and activate the virtual environment (venv)if it has not been activated previously.
        4.3 cd ./docs
        4.4 pytest -v
    4.5 Client test
        4.6 cd ./client
        4.7 npm test