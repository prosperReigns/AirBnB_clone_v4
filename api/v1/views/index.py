#!/usr/bin/python3
""" """

from api.v1.views import app_views
from flask import jsonify
from models import storage

@app_views.route('/status')
def show_status():
    """ """
    return jsonify({'status': 'OK'})

@app_views.route('/stats')
def get_stat():
    stats = {
            'amenities': storage.count('Amenity'),
            'cities': storage.count('City'),
            'state': storage.count('State'),
            'reviews': storage.count('Review'),
            'places': storage.count('Place'),
            'users': storage.count('User')
            }

    return jsonify(stats)
    
