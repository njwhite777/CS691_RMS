# from flask_user import UserMixin
# from flask_user.forms import RegisterForm
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators
from app import db


class MenuItem(db.Model):
    __tablename__ = 'MenuItem'
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(255), nullable=False, server_default='')
    price = db.Column(db.String(255), nullable=False, server_default='')
    active = db.Column(db.Float(), nullable=False, server_default='0')
    category = db.Column(db.String(255), nullable=False, server_default='')
    information = db.Column(db.String(255), nullable=False, server_default='')
    ingredients = db.Column(db.String(255), nullable=False, server_default='')
    allergy_information = db.Column(db.String(255), nullable=False, server_default='')

    # Relationships
    # roles = db.relationship('Role', secondary='Menu', backref=db.backref('Menu', lazy='dynamic'))

class Menu(db.Model):
    __tablename__ = 'Menu'
    id = db.Column(db.Integer, primary_key=True)
    menu_id = db.Column(db.Integer())
