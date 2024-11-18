import pika

from app import db
from app.decorators.connector import rabbitmq_connector
from app.models import Advertisement


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


def process_message(app, channel, method, properties, body):
    try:
        advertisement_id = int(body.decode())
        print(f" [x] Получен запрос на удаление объявления с ID: {advertisement_id}")

        # Создаем контекст приложения
        with app.app_context():
            advertisement = Advertisement.query.get(advertisement_id)
            if advertisement:
                db.session.delete(advertisement)
                db.session.commit()
                print(f"Объявление {advertisement_id} удалено.")
            else:
                print(f"Объявление с ID {advertisement_id} не найдено.")

        # Подтверждаем получение сообщения
        channel.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"Ошибка при обработке сообщения: {str(e)}")
        channel.basic_nack(delivery_tag=method.delivery_tag, requeue=True)


@rabbitmq_connector(queue_name='responseAdvertisementQueue')
def receive_orders(channel, app=None):
    from app import create_app
    if not app:
        app = create_app()

    channel.queue_declare(queue='responseAdvertisementQueue', durable=True)
    channel.basic_consume(queue='responseAdvertisementQueue',
                          on_message_callback=lambda ch, method, properties, body: process_message(app, ch, method,
                                                                                                   properties, body))

    print(' [*] Ожидаем сообщения. Для выхода нажмите CTRL+C')
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print(' [*] Выход...')
