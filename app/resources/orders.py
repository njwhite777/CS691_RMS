"""
Define the REST verbs relative to the MenuItems
"""
from flask_restful import Resource
from flask_restful import reqparse

from app.models.restaurant_models import *
from app.models.employee_models import *
from app.models.menuItem_models import *
from app.models.order_models import *

import json

parser = reqparse.RequestParser()
parser.add_argument('id',location=['json'], type=str, help='')
parser.add_argument('restaurant',location=['json'], type=str, help='')
parser.add_argument('total_price',location=['json'], type=str, help='')
parser.add_argument('items',dest='menu_items',location=['json'], type=str,action='append', help='')
parser.add_argument('tip',location=['json'], type=str,help='')

oaParser = reqparse.RequestParser()
oaParser.add_argument('employee_id',location=['form'],action='append', type=str, help='')
oaParser.add_argument('order_id',location=['form'], type=str, help='')
oaParser.add_argument('order_complete',location=['form'],default=False, type=str, help='')

class OrderResource(Resource):

    def post(self):
        args = parser.parse_args()
        print(args)
        o = Order(total_price=args.total_price,order_status=0,restaurant_id=args.restaurant,tip=args.tip)
        r = Restaurant.query.get(args.restaurant)
        db.session.add(o)
        db.session.commit()
        menu_items = args.menu_items[0]
        menu_items = json.loads(menu_items.replace("\'","\""))
        for key,value in menu_items.items():
            for i in range(value['count']):
                oi = OrderItems(menuItem_id=key,order_id=o.id)
                db.session.add(oi)
                db.session.commit()
        rdict = o.toDict()
        if(r):
            rdict['restaurant_name'] = r.name
        return rdict

class OrderAssignmentResource(Resource):

    def post(self):
        args = oaParser.parse_args()
        oa = OrderAssignments.query.filter(OrderAssignments.order_id==args.order_id).all()
        for a in oa:
            db.session.delete(a)
            db.session.commit()
        for eid in args.employee_id:
            oa = OrderAssignments(employee_id=eid,order_id=args.order_id)
            db.session.add(oa)
            o = oa.getOrder()
            o.order_status = 1
            db.session.commit()
        return {}


    def put(self):
        args = oaParser.parse_args()

        if(args.order_complete):
            o = Order.query.get(args.order_id)
            o.order_status=3
            db.session.commit()

            return {}

        oa = OrderAssignments.query.filter(OrderAssignments.order_id==args.order_id).all()
        for a in oa:
            db.session.delete(a)
            db.session.commit()
        for eid in args.employee_id:
            oa = OrderAssignments(employee_id=eid,order_id=args.order_id)
            db.session.add(oa)
            o = oa.getOrder()
            o.order_status = 1
            db.session.commit()
        return {}

    # This is unnecessary right now. No deleting order once it has been placed.
    # def delete(self):
    #   return {}

    # This is unnecessary right now. No modifying order once it has been placed.
    # def put(self):
        # return {}
