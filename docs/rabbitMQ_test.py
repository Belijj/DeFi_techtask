import asyncio
import pytest
import aio_pika

@pytest.mark.asyncio
async def test_rabbitmq_produce_consume():
    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")
    async with connection:
        channel = await connection.channel()
        
        queue = await channel.declare_queue("test_queue", durable=True)
        
        message_body = "test message"
        await channel.default_exchange.publish(
            aio_pika.Message(body=message_body.encode()),
            routing_key=queue.name,
        )

        incoming_message = await queue.get(timeout=5)
        assert incoming_message.body.decode() == message_body
        await incoming_message.ack()

        assert queue.declaration_result.message_count == 0
