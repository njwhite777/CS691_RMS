# from flask_user import UserMixin
# from flask_user.forms import RegisterForm
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators
from app import db

from sqlalchemy.orm import relationship
from sqlalchemy import func
from sqlalchemy.sql import label
import datetime

from app.models.menuItem_models import MenuItem

class Order(db.Model):
    __tablename__ = 'order'
    id          = db.Column(db.Integer, primary_key=True)
    total_price = db.Column(db.Float, nullable=False, server_default='')
    order_status= db.Column(db.Integer)
    order_placed= db.Column(db.DateTime,default=datetime.datetime.utcnow)
    tip         = db.Column(db.Float, nullable=False,server_default='')

    restaurant_id = db.Column(db.Integer,db.ForeignKey('restaurant.id', ondelete='CASCADE'))

    items = db.relationship('MenuItem',secondary="order_items",backref="order")
    assigned = db.relationship('Employee',secondary="order_assignments",backref=db.backref('order', lazy='dynamic'))

    def getAssignedIDs(self):
        return [ a.id for a in self.assigned ]

    def getMenuItems(self):
        return [ MenuItem.query.get(item.id) for item in self.items ]

    def toDict(self):
        return {
            'id' : self.id,
            'total_price': self.total_price,
            'order_status': self.order_status,
            'order_placed': self.order_placed.strftime("%Y-%m-%d %H:%M:%s")
        }

class OrderItems(db.Model):
    __tablename__ = 'order_items'
    id          = db.Column(db.Integer, primary_key=True)

    order_id    = db.Column(db.Integer,db.ForeignKey('order.id', ondelete='CASCADE'))
    menuItem_id = db.Column(db.Integer,db.ForeignKey('menu_item.id', ondelete='CASCADE'))

    def toDict(self):
        return {
            'id' : self.id,
            'order_id': self.order_id,
            'menuItems_id': self.menuItems_id
        }

class OrderAssignments(db.Model):
    __tablename__ = 'order_assignments'
    id = db.Column(db.Integer, primary_key=True)

    employee_id    = db.Column(db.Integer,db.ForeignKey('employee.id', ondelete='CASCADE'))
    order_id = db.Column(db.Integer,db.ForeignKey('order.id', ondelete='CASCADE'))

    def getOrder(self):
        return Order.query.filter(Order.id==self.order_id).first()

    def toDict(self):
        return {
            'id' : self.id,
            'order_id': self.order_id,
            'user_id': self.employee_id
        }
