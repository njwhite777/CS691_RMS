# from flask_user import UserMixin
# from flask_user.forms import RegisterForm
from sqlalchemy import Integer, ForeignKey, String, Column
from sqlalchemy.orm import relationship

from app.models.menuItem_models import *

from app import db

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, server_default='')

    items = relationship("ItemCategory",backref="category")
    menus = relationship("MenuCategories",backref="category")

    def toDict(self):
        return {

        }

class MenuCategories(db.Model):

    __tablename__ = 'menu_category'

    id = db.Column(db.Integer, primary_key=True)

    menu_id = db.Column(db.Integer, ForeignKey("menu.id"))
    category_id = db.Column(db.Integer, ForeignKey("category.id"))


class ItemCategory(db.Model):
    __tablename__ = 'menu_item_category'

    id = db.Column(db.Integer, primary_key=True)

    item_id = db.Column(db.Integer,ForeignKey("menu_item.id"))
    category_id = db.Column(db.Integer,ForeignKey("category.id"))
