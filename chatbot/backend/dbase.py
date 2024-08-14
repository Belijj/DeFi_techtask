import asyncpg
from typing import List, Tuple

class DataBase:
    def __init__(self):
        self._connection_pool = None

    async def connect(self):
        if not self._connection_pool:
            self._connection_pool = await asyncpg.create_pool(
                database="chatbot", 
                user="postgres", 
                password="3664b60403314c59ba7d55f9114383b3", 
                host="localhost", 
                port="5432",
                min_size=10,  
                max_size=100,
            )

    async def create_table(self):
        if not self._connection_pool:
            await self.connect()  
        async with self._connection_pool.acquire() as con:
            await con.execute('''
                CREATE TABLE IF NOT EXISTS Messages(
                    id SERIAL PRIMARY KEY,
                    message TEXT
                )
            ''')

    async def add_message(self, message: str):
        if not self._connection_pool:
            await self.connect()
        
        async with self._connection_pool.acquire() as con:
            try:
                await con.execute('''
                    INSERT INTO Messages(message) VALUES ($1)
                ''', message)
                print(f"Message added: {message}")
            except Exception as e:
                print(e)

    async def retrieve_messages(self):
        if not self._connection_pool:
            await self.connect()
        
        async with self._connection_pool.acquire() as con:
            rows = await con.fetch('''
                SELECT * FROM Messages ORDER BY id DESC LIMIT 5
            ''')
        return [(row['id'], row['message']) for row in rows]
    
    async def close(self):
        if self._connection_pool:
            await self._connection_pool.close()
