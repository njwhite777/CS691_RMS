from .menuItems import *
from .restaurant import *
from .orders import *
from .menu import *
from flask import Blueprint
from flask_restful import Api

def setupResources(api):
    api.add_resource(MenuItemResource,'/menuItem')
    api.add_resource(RestaurantResource,'/api/restaurant')
    api.add_resource(MenuResource,'/api/menu')
    api.add_resource(OrderResource,'/api/orders')
    api.add_resource(OrderAssignmentResource,'/api/order/assign')
