import pika
from functools import wraps


def rabbitmq_connector(queue_name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            credentials = pika.PlainCredentials('guest', 'guest')
            parameters = pika.ConnectionParameters('localhost', 5672, '/', credentials)
            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()
            channel.queue_declare(queue=queue_name, durable=True)
            result = func(channel, *args, **kwargs)
            connection.close()
            return result

        return wrapper

    return decorator
