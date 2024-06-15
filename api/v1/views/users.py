#!/usr/bin/python3
""" """

from flask import jsonify, request
from models.user import User
from models import storage
from api.v1.views import app_views


@app_views.route("/users", strict_slashes=False)
def get_user_status():
    """ """
    users = storage.all(User).values()

    lists = []

    for user in users:
        lists.append(user.to_dict())

    return jsonify(lists)


@app_views.route("/users/<user_id>", strict_slashes=False)
def get_user(user_id):
    """ """

    user = storage.get(User, user_id)

    if user:
        return jsonify(user.to_dict())
    else:
        abort(404)


@app_views.route("/users/<user_id>", methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """ """

    user = storage.get(User, user_id)

    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/users", methods=['POST'], strict_slashes=False)
def add_user(user_id):
    """ """
    if request.content_type != 'application/json':
        abort(404, 'Not a JSON')
    if not request.get_json():
        abort(404, 'Not a JSON')
    kwargs = request.get_json()

    if 'email' not in kwargs:
        abort(404, 'Missing email')
    if 'password' not in kwargs:
        abort(404, 'Missing password')

    user = User(**kwargs)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """ """
    if request.content_type != 'application/json':
        abort(404, 'Not a JSON')
    user = request.get(User, user_id)

    if user:
        if not request.get_json():
            abort(404, 'Not a JSON')
        data = request.get_json()
        ignore_keys = ['id', 'created_at', 'updated_at']

        for key, value in data.items():
            if key not in ignore_keys:
                setattr(user, key, value)
        user.save()
        return jsonify(user.to_dict()), 200
    else:
        abort(404)
