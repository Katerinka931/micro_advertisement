import os
import py_eureka_client.eureka_client as eureka_client

from flask import Flask, request, jsonify
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


@app.route('/api/advertisement')
def get_all_advertisements():
    advertisements = Advertisement.query.all()
    return jsonify([ad.dict() for ad in advertisements])


@app.route('/api/advertisement/<int:advertisement_id>')
def get_advertisement(advertisement_id):
    try:
        advertisement = Advertisement.query.get(advertisement_id)
        return jsonify(advertisement.dict()), 200
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


# def get_service_url():
#     serviceInstance = eureka_client.get_instance(EUREKA_SERVER, 'discussions')


@app.route('/api/advertisement/<int:advertisement_id>', methods=['DELETE'])
def delete_advertisement(advertisement_id):
    advertisement = Advertisement.query.get(advertisement_id)
    if advertisement is None:
        return jsonify({"message": "Объявление не найдено"}), 404

    db.session.delete(advertisement)
    db.session.commit()
    return jsonify({"message": "Объявление удалено"}), 200


if __name__ == '__main__':
    app.run()
