"""
Define the REST verbs relative to the MenuItems
"""

from flask_restful import Resource
from flask_restful import reqparse

parser = reqparse.RequestParser()

parser.add_argument('id',location=['form','json','values'], type=str, help='')
parser.add_argument('name',location=['form','json','values'], type=str, help='')

from flask.json import jsonify
from app.models.restaurant_models import *
import json

class RestaurantResource(Resource):
    """Verbs relative to a menu item"""

    def get(self):
        args = parser.parse_args()

        if(not(args.name) and not(args.id)):
            restaurants = Restaurant.query.filter().all()
            return [r.toDict() for r in restaurants]
        else:
            restaurants = Restaurant.query.filter(Restaurant.name==args.name).all()
            items = list()
            for restaurant in restaurants:
                items.append(restaurant.toDict())
        return items

    def post(self):
        """ Create a menu item based on the posted information """
        args = parser.parse_args()
        if(args.name):
            restaurant = Restaurant.query.filter(Restaurant.name==args.name).first()
            if(not restaurant):
                restaurant = Restaurant(name=args.name,picture_url=args.picture_url,menu_color=args.menu_color,)
                db.session.add(restaurant)
                db.session.commit()
                return restaurant.toDict()
            return restaurant.toDict()
        else:
            return {}

    def delete(self):
        return {}

    def put(self):
        return {}
