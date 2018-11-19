# from flask_user import UserMixin
# from flask_user.forms import RegisterForm
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators
from app import db


class MenuItem(db.Model):
    __tablename__ = 'menu_item'
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(255), nullable=False, server_default='')
    price = db.Column(db.String(255), nullable=False, server_default='')
    active = db.Column(db.Boolean(), nullable=False, server_default='0')
    category = db.Column(db.String(255), nullable=False, server_default='')
    information = db.Column(db.String(255), nullable=False, server_default='')
    ingredients = db.Column(db.String(255), nullable=False, server_default='')
    allergy_information = db.Column(db.String(255), nullable=False, server_default='')

class MenuItems(db.Model):
    __tablename__ = 'menu_items'
    menu_id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, primary_key=True)

class Menu(db.Model):
    __tablename__ = 'menu'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255),nullable=False)
