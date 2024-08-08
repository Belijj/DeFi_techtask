import subprocess
import os
import sys

def run_command(command, cwd=None, shell=False):
    """Выполняет команду и выводит её результат."""
    try:
        result = subprocess.run(command, cwd=cwd, shell=shell, check=True)
        print(f"Command '{' '.join(command)}' executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while executing command: {e}")
        sys.exit(1)

def main():
    # Запуск RabbitMQ
    print("Starting RabbitMQ...")
    rabbitmq_dir = os.path.join(os.getcwd(), 'rabbitmq')
    run_command(['docker-compose', 'up', '-d'], cwd=rabbitmq_dir)

    # Переход в директорию microservices
    print("Setting up microservices...")
    microservices_dir = os.path.join(os.getcwd(), 'microservices')
    
    # Активация виртуального окружения
    venv_activate = os.path.join(microservices_dir, 'venv', 'Scripts', 'activate')
    if not os.path.exists(venv_activate):
        print("Virtual environment not found. Please set it up first.")
        sys.exit(1)
    
    # Запуск data-generator.py в фоне
    print("Running data-generator.py...")
    run_command([sys.executable, 'data-generator.py'], cwd=microservices_dir)

    # Запуск socket-service.py
    print("Running socket-service.py...")
    run_command(['uvicorn', 'socket-service:app', '--host', '0.0.0.0', '--port', '8001'], cwd=microservices_dir)

    # Переход в директорию client
    print("Starting client application...")
    client_dir = os.path.join(os.getcwd(), 'client')
    run_command(['npm', 'start'], cwd=client_dir)

if __name__ == "__main__":
    main()
