# This file defines command line commands for manage.py
#
# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>

import datetime

from flask import current_app
from flask_script import Command

from app import db
from app.models.user_models import User, Role
from app.models.menuItem_models import Menu, MenuItem, MenuItems

class InitDbCommand(Command):
    """ Initialize the database."""

    def run(self):
        init_db()
        print('Database has been initialized.')

def init_db():
    """ Initialize the database."""
    db.drop_all()
    db.create_all()
    create_users()
    create_menu_item()


def create_users():
    """ Create users """

    # Create all tables
    db.create_all()

    # Adding roles
    admin_role = find_or_create_role('admin', u'Admin')
    staff_role = find_or_create_role('staff', u'Staff')

    # Add users
    user = find_or_create_user(u'Admin', u'Example', u'admin@example.com', 'Password1', admin_role)
    user = find_or_create_user(u'User', u'Example', u'user@example.com', 'Password1',staff_role)

    # Save to DB
    db.session.commit()

def create_menu_item():
    # Note: Assuming the db.create_all() command has already been called.
    find_or_create_menu("General")
    db.session.commit()
    find_or_create_menu_item("Risoto De Milano","27",active=True,category="Dinner",ingredients="Shrimp, mussle, scallops on rice.")
    find_or_create_menu_item("Shrimp Skampi","22",active=True,category="Dinner",ingredients="Shrimp, with white sauce on pasta.")
    find_or_create_menu_item("Spaghetti","22",active=True,category="Lunch",ingredients="Tomatoe sauce with meatballs on spaghetti pasta.")
    find_or_create_menu_item("Breadsticks","22",active=True,category="Appetizer",ingredients="Breadsticks.")
    find_or_create_menu_item("Eggplant Parmesean","25",active=False,category="Dinner",ingredients="Eggplant + Parmesean.")
    find_or_create_menu_item("Sushi","25",active=False,category="Appetizer",allergy_information="Seafood.",ingredients="Fish, rice, seaweed.",information="contains raw fish")
    db.session.commit()

def find_or_create_menu(name):
    menu = Menu.query.filter(Menu.name==name).first()
    if not menu:
        menu = Menu(name=name)
        db.session.add(menu)
    return menu

def find_or_create_menu_item(name,price,menu_name="General",active=None,category=None,information=None,ingredients=None,allergy_information=None):
    menu = Menu.query.filter(Menu.name==menu_name).first()
    menuItem = MenuItem.query.filter(MenuItem.name==name).first()
    if not menuItem:
        menuItem = MenuItem(name=name,price=price,active=active,category=category,information=information,ingredients=ingredients,allergy_information=allergy_information)
        db.session.add(menuItem)
        db.session.commit()
        menuItems = MenuItems(menu_id=menu.id,item_id=menuItem.id)
        db.session.add(menuItems)
        db.session.commit()
    return menuItem


def find_or_create_role(name, label):
    """ Find existing role or create new role """
    role = Role.query.filter(Role.name == name).first()
    if not role:
        role = Role(name=name, label=label)
        db.session.add(role)
    return role


def find_or_create_user(first_name, last_name, email, password, role=None):
    """ Find existing user or create new user """
    user = User.query.filter(User.email == email).first()
    if not user:
        user = User(email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password=current_app.user_manager.password_manager.hash_password(password),
                    active=True,
                    email_confirmed_at=datetime.datetime.utcnow())
        if role:
            user.roles.append(role)
        db.session.add(user)
    return user
