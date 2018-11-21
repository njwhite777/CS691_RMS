# from flask_user import UserMixin
# from flask_user.forms import RegisterForm
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators
from app import db

class Restaurant(db.Model):
    __tablename__ = 'restaurant'
    # Restaurant id
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(255), nullable=False, server_default='')
    picture_url = db.Column(db.String(255), nullable=False, server_default='')
    menu_color  = db.Column(db.String(255), nullable=False, server_default='')

    def toDict(self):
        return {
            'id' : self.id
            'name': self.name,
            'picture_url': self.picture_url,
            'menu_color': self.menu_color
        }

class RestaurantMenus(db.Model):
    __tablename__ = 'restaurant_menus'
    id = db.Column(db.Integer(), primary_key=True)
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id', ondelete='CASCADE'))
    restaurant_id = db.Column(db.Integer,db.ForeignKey('restaurant.id', ondelete='CASCADE'))
