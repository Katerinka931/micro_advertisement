import os

from flask import Flask, request, jsonify
from models import db, Advertisement

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1@localhost:1978/microAdvertisements'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.debug = True

with app.app_context():
    # Если надо поменять уже существующую бд, то использовать инструмент переноса Alembic!
    db.create_all()


@app.route('/advertisement')
def get_all_advertisements():
    advertisements = Advertisement.query.all()
    return jsonify([ad.dict() for ad in advertisements])


@app.route('/advertisement/<int:advertisement_id>')
def get_advertisement(advertisement_id):
    try:
        advertisement = Advertisement.query.get(advertisement_id)
        return jsonify(advertisement.dict()), 200
    except AttributeError:
        return jsonify({"message": "Такого объявления не существует"}), 400


@app.route('/advertisement', methods=['POST'])
def add_advertisement():
    try:
        data = request.get_json()
        new_advertisement = Advertisement(data['title'], data['description'], data['price'], data['phone'])
        db.session.add(new_advertisement)
        db.session.commit()
        return jsonify({"message": "Объявление создано", "data": data}), 201
    except Exception as e:
        return jsonify({"message": "Ошибка при создании объявления"}), 400


@app.route('/advertisement/<int:advertisement_id>', methods=['DELETE'])
def delete_advertisement(advertisement_id):
    advertisement = Advertisement.query.get(advertisement_id)
    if advertisement is None:
        return jsonify({"message": "Объявление не найдено"}), 404

    db.session.delete(advertisement)
    db.session.commit()
    return jsonify({"message": "Объявление удалено"}), 200


if __name__ == '__main__':
    app.run()
