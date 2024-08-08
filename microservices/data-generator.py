import aio_pika
import asyncio
import json
import random
import string

async def connect_to_rabbitmq():
    while True:
        try:
            connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")
            print("Conn OK")
            return connection
        except aio_pika.exceptions.AMQPConnectionError as e:
            print(f"Conn failed: {e}. Retry in 5 sec")
            await asyncio.sleep(5)

async def generate_data():
    connection = await connect_to_rabbitmq()
    
    async with connection:
        async with connection.channel() as channel:
            while True:
                msg = generate_message()
                data = {"message": msg}
                try:
                    await channel.default_exchange.publish(
                        aio_pika.Message(body=json.dumps(data).encode()),
                        routing_key='data_queue',
                    )
                    print(f"Msg published: {data}")
                except aio_pika.exceptions.AMQPError as e:
                    print(f"Failed to publish msg: {e}. Retry in 5 sec")
                    await asyncio.sleep(5)
                await asyncio.sleep(5)

def generate_message():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

if __name__ == "__main__":
    asyncio.run(generate_data())
