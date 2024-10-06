import os
import requests

from py_eureka_client import eureka_client
from flask import Flask, request, jsonify
from broker_pub import send_order
from models import db, Advertisement

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1@localhost:1978/microAdvertisements'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

EUREKA_SERVER = "http://localhost:8761/eureka"
eureka_client.init(eureka_server=EUREKA_SERVER,
                   app_name="advertisement",
                   instance_id="advertisement-instance",
                   instance_port=5000,
                   instance_host="127.0.0.1")

db.init_app(app)
app.debug = True
with app.app_context():
    # Если надо поменять уже существующую бд, то использовать инструмент переноса Alembic!
    db.create_all()


async def get_service_address_by_service_name(service):
    """Получение адреса микросервиса по его названию"""
    applications = await eureka_client.get_applications(EUREKA_SERVER)
    instance = applications.get_application(service).instances[0]
    return instance.homePageUrl


@app.route('/api/advertisement')
def get_all_advertisements():
    advertisements = Advertisement.query.all()
    return jsonify([ad.dict() for ad in advertisements])


@app.route('/api/advertisement/<int:advertisement_id>')
async def get_advertisement(advertisement_id):
    url = await get_service_address_by_service_name('DISCUSSIONS')  # todo как-то по-другому? если останется время
    count = requests.get(f'{url}api/forum/discussions/count_advertisement/{advertisement_id}').text

    try:
        advertisement = Advertisement.query.get(advertisement_id)
        advertisement_dict = advertisement.dict()
        advertisement_dict.update({'count': count})
        return jsonify(advertisement_dict), 200
    except AttributeError:
        return jsonify({"message": "Такого объявления не существует"}), 400


@app.route('/api/advertisement', methods=['POST'])
def add_advertisement():
    try:
        data = request.get_json()
        new_advertisement = Advertisement(data['title'], data['description'], data['price'], data['phone'])
        db.session.add(new_advertisement)
        db.session.commit()
        return jsonify({"message": "Объявление создано", "data": data}), 201
    except Exception as e:
        return jsonify({"message": "Ошибка при создании объявления"}), 400


@app.route('/api/advertisement/<int:advertisement_id>', methods=['DELETE'])
def delete_advertisement(advertisement_id):
    advertisement = Advertisement.query.get(advertisement_id)
    if advertisement is None:
        return jsonify({"message": "Объявление не найдено"}), 404

    send_order(advertisement_id)

    db.session.delete(advertisement)
    db.session.commit()
    return jsonify({"message": "Объявление удалено"}), 200


if __name__ == '__main__':
    app.run()
