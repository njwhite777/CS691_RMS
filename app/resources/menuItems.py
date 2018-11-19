"""
Define the REST verbs relative to the MenuItems
"""

from flask_restful import Resource
from flask_restful import reqparse

parser = reqparse.RequestParser()

parser.add_argument('id',location=['form','json','values'], type=str, help='')
parser.add_argument('name',location=['form','json','values'], type=str, help='')
parser.add_argument('price',location=['form', 'json'], type=str, help='')
parser.add_argument('allergy_information',location=['form', 'json'], type=str, help='')
parser.add_argument('information',location=['form', 'json'], type=str, help='')
parser.add_argument('ingredients',location=['form', 'json'], type=str, help='')
parser.add_argument('active',location=['form', 'json'], type=bool, help='')
parser.add_argument('category',location=['form', 'json'], type=bool, help='')

from flask.json import jsonify
from app.models.menuItem_models import *
import json

class MenuResource(Resource):

    @staticmethod
    def post(name=None):
        pass

    @staticmethod
    def put(name=None):
        pass

class MenuItemResource(Resource):
    """Verbs relative to a menu item"""

    def get(self):
        args = parser.parse_args()
        menuItems = MenuItem.query.filter().all()
        items = list()
        for item in menuItems:
            items.append({
                'name': item.name,
                'price': item.price,
                'information': item.information,
                'allergy_information' : item.allergy_information
            })
        return jsonify(items)

    def post(self):
        """ Create a menu item based on the posted information """
        print("HERE!!!")
        args = parser.parse_args()
        if(args.name):
            print("HERE!!!")
            menuItem = MenuItem(name=args.name,price=args.price,active=True,category=args.category,information=args.information,ingredients=args.ingredients,allergy_information=args.allergy_information)
            return json.dumps(menuItem.toDict())
        else:
            print("problem")
            return json.dumps({})

    @staticmethod
    def put():
        """ Edit a menu item based on the posted information """
        menuItem = None
        args = parser.parse_args()
        if(args.id):
            menuItem = MenuItem.query.get(args.id)
        elif(args.name):
            menuItem = MenuItem.query.get(args.id)
        return json.dumps()
