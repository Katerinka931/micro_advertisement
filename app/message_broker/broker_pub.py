import pika

from app.decorators.connector import rabbitmq_connector


@rabbitmq_connector(queue_name='advertisement')
def send_order(channel, data):
    channel.basic_publish(
        exchange='',
        routing_key='advertisement',
        body=str(data),
        properties=pika.BasicProperties(
            content_type='text/plain',
            delivery_mode=2
        ),
        mandatory=True
    )
