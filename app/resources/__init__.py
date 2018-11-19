from .menuItems import *
from flask import Blueprint
from flask_restful import Api

def setupResources(api):
    api.add_resource(MenuItemResource,'/menuItem')
