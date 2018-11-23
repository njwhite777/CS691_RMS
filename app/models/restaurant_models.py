# from flask_user import UserMixin
# from flask_user.forms import RegisterForm
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators
from sqlalchemy.orm import relationship
from sqlalchemy import and_, or_

from app import db
from app.models.employee_models import Employee,EmployeeTimeCard
from app.models.menuItem_models import *
from app.models.order_models import Order

import datetime

class Restaurant(db.Model):
    __tablename__ = 'restaurant'
    # Restaurant id
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(255), nullable=False, server_default='')
    picture_url = db.Column(db.String(255), nullable=False, server_default='')
    tagline  = db.Column(db.String(255), nullable=False, server_default='')

    def getEmployees(self):
        res = RestaurantEmployees.query.filter(RestaurantEmployees.restaurant_id==self.id).all()
        employees = list()
        for employee in res:
            e = Employee.query.filter(Employee.id==employee.employee_id).first()
            if(e):
                employees.append(e)
        return employees

    def getEmployeeIds(self):
        return [ e.id for e in self.getEmployees() ]

    def getAssignees(self):
        assignee = EmployeeTimeCard.query.filter(and_(*[EmployeeTimeCard.restaurant_id==self.id,EmployeeTimeCard.time_in<datetime.datetime.utcnow()])).all()
        return [ Employee.query.filter(Employee.id==a.employee_id).first() for a in assignee ]

    def getRestaurantMenu(self):
        return RestaurantMenus.query.filter(RestaurantMenus.restaurant_id==self.id).first()

    def getMenuID(self):
        m = self.getRestaurantMenu()
        if(m):
            return m.menu_id
        return None

    def getMenu(self):
        rm = self.getRestaurantMenu()
        m = Menu.query.get(rm.menu_id)
        if(m):
            return m
        return None

    def getOrderByStatus(self,order_status=0):
        return Order.query.filter(and_(*[Order.restaurant_id==self.id,Order.order_status==order_status])).all()

    def toDict(self):
        res = RestaurantEmployees.query.filter(RestaurantEmployees.restaurant_id==self.id).all()
        employees = list()
        for employee in res:
            e = Employee.query.filter(Employee.id==employee.employee_id).first()
            if(e):
                employees.append(e.toDict())

        return {
            'id' : self.id,
            'name': self.name,
            'picture_url': self.picture_url,
            'tagline': self.tagline,
            'employees': employees
        }

class RestaurantMenus(db.Model):
    __tablename__ = 'restaurant_menus'
    id = db.Column(db.Integer(), primary_key=True)
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id', ondelete='CASCADE'))
    restaurant_id = db.Column(db.Integer,db.ForeignKey('restaurant.id', ondelete='CASCADE'))

    def toDict(self):
        return {
            'id' : self.id,
            'menu_id': self.menu_id,
            'restaurant_id': self.restaurant_id
        }

class RestaurantEmployees(db.Model):
    __tablename__ = 'restaurant_employee'
    id = db.Column(db.Integer(), primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id', ondelete='CASCADE'))
    restaurant_id = db.Column(db.Integer,db.ForeignKey('restaurant.id', ondelete='CASCADE'))

    def toDict(self):
        return {
            'id' : self.id,
            'employee_id': self.employee_id,
            'restaurant_id': self.restaurant_id
        }
