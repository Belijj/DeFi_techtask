import psycopg2

def connect_to_postgres():
    # Подключение к базе данных
    conn = psycopg2.connect(
        dbname="chatbot", 
        user="postgres", 
        password="3664b60403314c59ba7d55f9114383b3", 
        host="localhost", 
        port="5432"
    )
    
    # Создание курсора для выполнения запросов
    cur = conn.cursor()

    # Выполнение запроса
    cur.execute("SELECT version();")
    db_version = cur.fetchone()
    print(f"PostgreSQL version: {db_version[0]}")

    # Закрытие курсора и соединения
    cur.close()
    conn.close()

if __name__ == "__main__":
    connect_to_postgres()
