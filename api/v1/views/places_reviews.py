#!/usr/bin/python3
""" """

from flask import jsonify, request
from models.city import City
from models.review import Review
from models import storage
from api.v1.views import app_views


@app_views.route("/cities/<city_id>/reviews", strict_slashes=False)
def get_review_status(city_id):
    """ """
    city = storage.all(City, city_id)

    lists = []

    for city in city.reviews:
        lists.append(city.to_dict())

    return jsonify(lists)


@app_views.route("/reviews/<review_id>", strict_slashes=False)
def get_review(review_id):
    """ """

    review = storage.get(Review, review_id)

    if review:
        return jsonify(review.to_dict())
    else:
        abort(404)


@app_views.route("/reviews/<review_id>", methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """ """

    review = storage.get(Review, review_id)

    if review:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/places/<place_id>/reviews", methods=['POST'],
                                        strict_slashes=False)
def add_review(place_id):
    """ """
    if request.content_type != 'application/json':
        abort(404, 'Not a JSON')

    place = storage.get(Place, place_id)
    if not place:
        return abort(404)
    if not request.get_json():
        abort(404, 'Not a JSON')
    kwargs = request.get_json()

    if 'user_id' not in kwargs:
        abort(404, 'Missing user_id')
    if 'text' not in kwargs:
        abort(404, 'Missing text')
    kwargs['place_id'] = place_id

    review = Review(**kwargs)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=['PUT'],
                                strict_slashes=False)
def update_review(review_id):
    """ """
    if request.content_type != 'application/json':
        abort(404, 'Not a JSON')
    review = request.get(Review, review_id)

    if review:
        if not request.get_json():
            abort(404, 'Not a JSON')
        data = request.get_json()
        ignore_keys = ['id', 'place_id', 'created_at', 'updated_at']

        for key, value in data.items():
            if key not in ignore_keys:
                setattr(review, key, value)
        review.save()
        return jsonify(review.to_dict()), 200
    else:
        abort(404)
