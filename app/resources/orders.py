"""
Define the REST verbs relative to the MenuItems
"""

from flask_restful import Resource
from flask_restful import reqparse

parser = reqparse.RequestParser()

parser.add_argument('id',location=['json'], type=str, help='')
parser.add_argument('restaurant',location=['json'], type=str, help='')
parser.add_argument('total_price',location=['json'], type=str, help='')
parser.add_argument('items',location=['json'], type=str,action='append', help='')

from flask.json import jsonify
from app.models.restaurant_models import *
from app.models.employee_models import *
from app.models.menuItem_models import *
import json

class OrderResource(Resource):

    def get(self):
        return {}

    def post(self):
        args = parser.parse_args()
        # {'id': None, 'restaurant': '1',
        #   'items': ["{'5': {'count': 1, 'name': 'Eggplant Parmesean'},
        #               '1': {'count': 1, 'name': 'Risoto De Milano'},
        #               '3': {'count': 1, 'name': 'Spaghetti'}}"],
        #   'total_price': '74'}
        print(args)
        return {}

    def delete(self):
        return {}

    def put(self):
        return {}
