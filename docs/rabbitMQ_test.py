import asyncio
import pytest
import aio_pika

@pytest.mark.asyncio
async def test_rabbitmq_produce_consume():
    # Connect to RabbitMQ
    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")
    async with connection:
        channel = await connection.channel()
        
        # Declare queue
        queue = await channel.declare_queue("test_queue", durable=True)
        
        # Publish a message
        message_body = "test message"
        await channel.default_exchange.publish(
            aio_pika.Message(body=message_body.encode()),
            routing_key=queue.name,
        )

        # Consume the message
        incoming_message = await queue.get(timeout=5)
        assert incoming_message.body.decode() == message_body
        await incoming_message.ack()

        # Ensure the queue is empty now
        assert queue.declaration_result.message_count == 0
