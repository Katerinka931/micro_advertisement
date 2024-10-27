import asyncio
import requests

from flask import request, jsonify
from .init import advertisement_bp
from ..config import EUREKA_SERVER
from ..database import db
from app.decorators.require_role import role_required
from ..message_broker.broker_pub import send_order
from ..models import Advertisement
from ..utils import get_service_address_by_service_name


@advertisement_bp.route('/api/advertisement', methods=['GET'])
@role_required('read')
def get_all_advertisements():
    advertisements = Advertisement.query.all()
    return jsonify([ad.dict() for ad in advertisements])


@advertisement_bp.route('/api/advertisement/<int:advertisement_id>', methods=['GET'])
@role_required('read')
def get_advertisement(advertisement_id):
    url = asyncio.run(get_service_address_by_service_name('DISCUSSIONS', EUREKA_SERVER))
    count = requests.get(f'{url}api/forum/discussions/count_advertisement/{advertisement_id}').text

    advertisement = Advertisement.query.get(advertisement_id)
    if advertisement is None:
        return jsonify({"message": "Такого объявления не существует"}), 404

    advertisement_dict = advertisement.dict()
    advertisement_dict.update({'count': count})
    return jsonify(advertisement_dict), 200


@advertisement_bp.route('/api/advertisement', methods=['POST'])
@role_required('write')
def add_advertisement():
    try:
        data = request.get_json()
        new_advertisement = Advertisement(title=data['title'], description=data['description'], price=data['price'],
                                          phone=data['phone'])
        db.session.add(new_advertisement)
        db.session.commit()
        return jsonify({"message": "Объявление создано", "data": data}), 201
    except Exception as e:
        return jsonify({"message": "Ошибка при создании объявления"}), 400


@advertisement_bp.route('/api/advertisement/<int:advertisement_id>', methods=['DELETE'])
@role_required('delete')
def delete_advertisement(advertisement_id):
    advertisement = Advertisement.query.get(advertisement_id)
    if advertisement is None:
        return jsonify({"message": "Объявление не найдено"}), 404

    send_order(advertisement_id)

    db.session.delete(advertisement)
    db.session.commit()
    return jsonify({"message": "Объявление удалено"}), 200
