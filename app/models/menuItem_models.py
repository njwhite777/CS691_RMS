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

    def containsRawMeat(self):
        ingredients = self.information.lower()
        return "raw beef" in ingredients or "raw chicken" in ingredients or "raw fish" in ingredients or "raw pork" in ingredients or "raw egg" in ingredients

    def toDict(self):
        return {
            'name': self.name,
            'price': self.price,
            'active': self.active,
            'category': self.category,
            'information': self.information,
            'ingredients': self.ingredients,
            'allergy_information': self.allergy_information,
        }

class MenuItems(db.Model):
    __tablename__ = 'menu_items'
    id = db.Column(db.Integer, primary_key=True)
    menu_id = db.Column(db.Integer,db.ForeignKey('menu.id', ondelete='CASCADE'))
    item_id = db.Column(db.Integer,db.ForeignKey('menu_item.id', ondelete='CASCADE'))

class Menu(db.Model):
    __tablename__ = 'menu'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255),nullable=False)
