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
        args = parser.parse_args()
        print(args)
        if(args.name):
            mi = MenuItem.query.filter(MenuItem.name==args.name).first()
            if(not mi):
                menuItem = MenuItem(name=args.name,price=args.price,active=args.active,category=args.category,information=args.information,ingredients=args.ingredients,allergy_information=args.allergy_information)
                db.session.add(menuItem)
                db.session.commit()
                mis = MenuItems(item_id=menuItem.id,menu_id=1)
                db.session.add(mis)
                db.session.commit()
                return menuItem.toDict()
            return mi.toDict()
        else:
            print("problem")
            return {}

    def put(self):
        """ Edit a menu item based on the posted information """
        args = parser.parse_args()
        if(args.id):
            mi = MenuItem.query.get(args.id)
            if(not mi):
                return {}
            for key,value in args.items():
                print(key,value)
                if(value):
                    setattr(mi,key,value)
            db.session.add(mi)
            db.session.commit()
            return mi.toDict()
        return {}
