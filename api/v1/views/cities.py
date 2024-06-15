#!/usr/bin/python3
""" """

from flask import jsonify, request
from models.city import City
from models.state import State
from models import storage
from api.v1.views import app_views


@app_views.route("/state/<state_id>/cities", strict_slashes=False)
def get_city_status(state_id):
    """ """
    state = storage.all(State, state_id)

    lists = []

    for city in state.cities:
        lists.append(city.to_dict())

    return jsonify(lists)


@app_views.route("/cities/<city_id>", strict_slashes=False)
def get_city(city_id):
    """ """

    city = storage.get(cities, city_id)

    if city:
        return jsonify(city.to_dict())
    else:
        abort(404)


@app_views.route("/cities/<city_id>", methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """ """

    city = storage.get(Cities, city_id)

    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/state/<state_id>/cities", methods=['POST'],
                                        strict_slashes=False)
def add_city(state_id):
    """ """
    if request.content_type != 'application/json':
        abort(404, 'Not a JSON')

    state = storage.get(State, state_id)
    if not state:
        return abort(404)
    if not request.get_json():
        abort(404, 'Not a JSON')
    kwargs = request.get_json()

    if 'name' not in kwargs:
        abort(404, 'Missing name')
    kwargs['state_id'] = state_id

    city = City(**kwargs)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=['PUT'],
                                strict_slashes=False)
def update_city(city_id):
    """ """
    if request.content_type != 'application/json':
        abort(404, 'Not a JSON')
    city = request.get(City, city_id)

    if city:
        if not request.get_json():
            abort(404, 'Not a JSON')
        data = request.get_json()
        ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']

        for key, value in data.items():
            if key not in ignore_keys:
                setattr(city, key, value)
        city.save()
        return jsonify(city.to_dict()), 200
    else:
        abort(404)
