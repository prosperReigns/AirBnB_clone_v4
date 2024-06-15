#!/usr/bin/python3
""" """

from flask import jsonify, request
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views


@app_views.route("/amenities", strict_slashes=False)
def get_amenity_status():
    """ """
    amenities = storage.all(Ameniy).items()

    lists = []

    for key, value in amenities:
        lists.append(value.to_dict())

    return jsonify(lists)


@app_views.route("/amenities/<amenity_id>", strict_slashes=False)
def get_amenity(amenity_id):
    """ """

    amenity = storage.get(Amenity, amenity_id)

    if amenity:
        return jsonify(amenity.to_dict())
    else:
        abort(404)


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """ """

    amenity = storage.get(Amenity, city_id)

    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/amenities", methods=['POST'], strict_slashes=False)
def add_amenity(amenity_id):
    """ """
    if request.content_type != 'application/json':
        abort(404, 'Not a JSON')
    if not request.get_json():
        abort(404, 'Not a JSON')
    kwargs = request.get_json()

    if 'name' not in kwargs:
        abort(404, 'Missing name')

    amenity = Amenity(**kwargs)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """ """
    if request.content_type != 'application/json':
        abort(404, 'Not a JSON')
    amenity = request.get(Amenity, amenity_id)

    if amenity:
        if not request.get_json():
            abort(404, 'Not a JSON')
        data = request.get_json()
        ignore_keys = ['id', 'created_at', 'updated_at']

        for key, value in data.items():
            if key not in ignore_keys:
                setattr(amenity, key, value)
        amenity.save()
        return jsonify(amenity.to_dict()), 200
    else:
        abort(404)
