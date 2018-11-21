# from flask_user import UserMixin
# from flask_user.forms import RegisterForm
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators
from app import db

class Order(db.Model):
    __tablename__ = 'order'
    id          = db.Column(db.Integer, primary_key=True)
    total_price = db.Column(db.Float, nullable=False, server_default='')
    order_status= db.Column(db.Integer)
    order_placed= db.Column(db.DateTime)

    def toDict(self):
        return {
            'id' : self.id,
            'total_price': self.total_price,
            'order_status': self.order_status,
            'order_placed': self.order_placed
        }

class OrderItems(db.Model):
    __tablename__ = 'order_items'
    id          = db.Column(db.Integer, primary_key=True)
    order_id    = db.Column(db.Integer,db.ForeignKey('order.id', ondelete='CASCADE'))
    menuItems_id = db.Column(db.Integer,db.ForeignKey('menu_items.id', ondelete='CASCADE'))

    def toDict(self):
        return {
            'id' : self.id,
            'order_id': self.order_id,
            'menuItems_id': self.menuItems_id
        }

class OrderAssignments(db.Model):
    __tablename__ = 'order_assignments'
    id = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer,db.ForeignKey('employee.id', ondelete='CASCADE'))
    order_id = db.Column(db.Integer,db.ForeignKey('order.id', ondelete='CASCADE'))

    def toDict(self):
        return {
            'id' : self.id,
            'order_id': self.order_id,
            'user_id': self.user_id
        }
