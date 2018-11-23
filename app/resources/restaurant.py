"""
Define the REST verbs relative to the MenuItems
"""

from flask_restful import Resource
from flask_restful import reqparse

parser = reqparse.RequestParser()

parser.add_argument('id',location=['form'], type=str, help='')
parser.add_argument('name',location=['form'], type=str, help='')
parser.add_argument('picture_url',location=['form'], type=str, help='')
parser.add_argument('tagline',location=['form'], type=str, help='')
parser.add_argument('employees',location=['form'], type=str,action='append', help='')
parser.add_argument('menu',location=['form'], type=str, help='')
parser.add_argument('tagline_options',location=['form'], type=str, help='')

from flask.json import jsonify
from app.models.restaurant_models import *
from app.models.employee_models import *
from app.models.menuItem_models import *
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
        print(args)
        if(args.name):
            restaurant = Restaurant.query.filter(Restaurant.name==args.name).first()
            if(not restaurant):
                restaurant = Restaurant(name=args.name,picture_url=args.picture_url,tagline=args.tagline,tagline_options=args.tagline_options)
                db.session.add(restaurant)
                db.session.commit()

                # Add users
                for employee in args.employees:
                    e = Employee.query.get(employee)
                    if(not(e)):
                        break
                    re = RestaurantEmployees(employee_id=e.id,restaurant_id=restaurant.id)
                    db.session.add(re)

                m  = Menu.query.filter(Menu.name==args.menu).first()
                rm = RestaurantMenus(menu_id=m.id,restaurant_id=restaurant.id)

                db.session.commit()
                return restaurant.toDict()
            return restaurant.toDict()
        else:
            return {}

    def delete(self):
        args = parser.parse_args()
        print(args)
        if(not(args.name) and not(args.id)):
            return {}
        elif(args.id):
            print("DELETING")
            r = Restaurant.query.get(args.id)
            db.session.delete(r)
            db.session.commit()
            return r.toDict()
        else:
            print("DELETING")
            r = Restaurant.query.filter(Restaurant.name==args.name).first()
            db.session.delete(r)
            db.session.commit()
            return r.toDict()
        return {}

    def put(self):
        args = parser.parse_args()
        print("PUT")
        print(args)
        if(args.id):
            r = Restaurant.query.get(args.id)
            res = RestaurantEmployees.query.filter(RestaurantEmployees.restaurant_id==args.id).all()

            for key,val in args.items():
                if(hasattr(r,key)):
                    setattr(r,key,val)

            for re in res:
                db.session.delete(re)

            for i in args.employees:
                re = RestaurantEmployees(restaurant_id=r.id,employee_id=i)
                db.session.add(re)

            rm = RestaurantMenus.query.filter(RestaurantMenus.restaurant_id==r.id).first()
            rm.menu_id = args.menu

            db.session.commit()
            return r.toDict()

        return {}
