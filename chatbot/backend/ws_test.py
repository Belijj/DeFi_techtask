import pytest
import asyncio
import websockets
import time
from random import randrange

NUM_USERS = 1000

TARGET_MESSAGES_PER_SECOND = 100

MESSAGE_INTERVAL = NUM_USERS / TARGET_MESSAGES_PER_SECOND

TEST_DURATION = 60

@pytest.mark.asyncio
async def test_simulate_multiple_users():
    start_time = time.time()
    user_tasks = [simulate_user(start_time) for _ in range(NUM_USERS)]
    
    await asyncio.gather(*user_tasks)

async def simulate_user(start_time):
    client_id = randrange(10000)
    url = f"ws://localhost:8080/ws/{client_id}"
    async with websockets.connect(url) as websocket:
        end_time = start_time + TEST_DURATION
        try:
            while time.time() < end_time:
                test_message = f"Message from client {client_id}"
                await websocket.send(test_message)
                print(f"Client {client_id} sent: {test_message}")
            
                await asyncio.sleep(MESSAGE_INTERVAL)
        except (websockets.ConnectionClosedError, Exception) as e:
            print(f"Client {client_id} encountered an error: {e}")

if __name__ == "__main__":
    pytest.main()
