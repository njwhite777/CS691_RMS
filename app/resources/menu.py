"""
Define the REST verbs relative to the MenuItems
"""

from flask_restful import Resource
from flask_restful import reqparse

parser = reqparse.RequestParser()

parser.add_argument('id',location=['form'], type=str, help='')
parser.add_argument('name',location=['form'], type=str, help='')
parser.add_argument('menu_items',location=['form'], type=str,action='append', help='')

from flask.json import jsonify
from app.models.menuItem_models import *
from app.models.employee_models import *
import json

class MenuResource(Resource):
    """Verbs relative to a menu item"""

    def get(self):
        pass

    def post(self):
        """ Create a menu based on the posted information """
        args = parser.parse_args()
        if(args.name):
            m = Menu.query.filter(Menu.name==args.name).first()
            if(not m):
                m = Menu(name=args.name)
                db.session.add(m)
                db.session.commit()
                for item_id in args.menu_items:
                    mi = MenuItems(menu_id=m.id,item_id=item_id)
                    db.session.add(mi)
                db.session.commit()
                return m.toDict()
            return m.toDict()
        else:
            return {}

    def delete(self):
        args = parser.parse_args()
        if(not(args.name) and not(args.id)):
            print("DELETING")
            return {}
        elif(args.id):
            m = Menu.query.get(args.id)
            db.session.delete(m)
            db.session.commit()
            return m.toDict()
        else:
            m = Menu.query.filter(Menu.name==args.name).first()
            db.session.delete(m)
            db.session.commit()
            return m.toDict()
        return {}

    def put(self):
        args = parser.parse_args()
        print(args)
        if(args.id):
            m = Menu.query.get(args.id)
            mis = MenuItems.query.filter(MenuItems.menu_id==m.id).all()
            for key,val in args.items():
                if(hasattr(m,key)):
                    setattr(m,key,val)
            for mi in mis:
                db.session.delete(mi)
            for i in args.menu_items:
                mi = MenuItems(menu_id=m.id,item_id=i)
                db.session.add(mi)


                #     db.session.delete(mi)
            db.session.commit()
            return m.toDict()

        return {}
