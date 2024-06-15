#!/usr/bin/python3
""" """

from flask import jsonify, request
from models.place import Place
from models.city import City
from models import storage
from api.v1.views import app_views


@app_views.route("/cities/<city_id>/places", strict_slashes=False)
def get_place_in_city(city_id):
    """ """
    city = storage.get(Cities, city_id)

    if not city:
        abort(404)


    lists = []

    for place in city.places:
        lists.append(place.to_dict())

    return jsonify(lists)


@app_views.route("/places/<place_id>/places", strict_slashes=False)
def get_place(place_id):
    """ """

    place = storage.get(Place, place_id)

    if place:
        return jsonify(place.to_dict())
    else:
        abort(404)


@app_views.route("/places/<place_id>", methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """ """

    place = storage.get(Place, place_id)

    if place:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/cities/<city_id>/places", methods=['POST'], strict_slashes=False)
def add_place(city_id):
    """ """
    city = storage.get(Cities, city_id)

    if not city:
        abort(404)

    if not request.get_json():
        abort(404, 'Not a JSON')

    date = request.get_json()
    if 'user_id' not in data:
        abort(404, 'Missing user_id')
    if 'name' not in date:
        abort(404, 'Missing name')

    user = storage.get(User, data['user_id'])
    if not user:
        return abort(404)

    data['city_id'] = city_id
    place = Place(**data)
    place.save()

    return jsonify(place.to_dicy()), 201


@app_views.route("/places/<place_id>", methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ """
    place = request.get(Place, place_id)

    if place:
        if not request.get_json():
            abort(404, 'Not a JSON')
        data = request.get_json()
        ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']

        for key, value in data.items():
            if key not in ignore_keys:
                setattr(place, key, value)
        place.save()
        return jsonify(place.to_dict()), 200
    else:
        abort(404)
