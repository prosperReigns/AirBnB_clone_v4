#!/usr/bin/python3
""" """

from flask import jsonify, request
from models.state import State
from models import storage
from api.v1.views import app_views


@app_views.route("/states", strict_slashes=False)
def get_status():
    """ """
    states = storage.all(State).values()

    lists = []

    for state in states:
        state.append(state.to_dict())

    return jsonify(lists)


@app_views.route("/states/<state_id>", strict_slashes=False)
def get_state(state_id):
    """ """

    state = storage.get(State, state_id)

    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)


@app_views.route("/states/<state_id>", methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """ """

    state = storage.get(State, state_id)

    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/states", methods=['POST'], strict_slashes=False)
def add_state(state_id):
    """ """
    if request.content_type != 'application/json':
        abort(404, 'Not a JSON')
    if not request.get_json():
        abort(404, 'Not a JSON')
    kwargs = request.get_json()

    if 'name' not in kwargs:
        abort(404, 'Missing name')

    states = States(**kwargs)
    states.save()
    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>", methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """ """
    if request.content_type != 'application/json':
        abort(404, 'Not a JSON')
    state = request.get(State, state_id)

    if state:
        if not request.get_json():
            abort(404, 'Not a JSON')
        data = request.get_json()
        ignore_keys = ['id', 'created_at', 'updated_at']

        for key, value in data.items():
            if key not in ignore_keys:
                setattr(state, key, value)
        state.save()
        return jsonify(state.to_dict())
    else:
        abort(404)
