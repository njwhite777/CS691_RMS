# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>


from flask import Blueprint, redirect, render_template
from flask import request, url_for
from flask_user import current_user, login_required, roles_required

from app import db
from app.models.user_models import UserProfileForm
from app.models.menuItem_models import Menu, MenuItem, MenuItems


main_blueprint = Blueprint('main', __name__, template_folder='templates')

# The Home page is accessible to anyone
@main_blueprint.route('/')
def home_page():
    return redirect('/menu')

# The Home page is accessible to anyone
@main_blueprint.route('/_users')
def users_page():
    return render_template('main/_users.html')

# The User page is accessible to authenticated users (users that have logged in)
@main_blueprint.route('/menu')
@main_blueprint.route('/menu/<int:id>',defaults = {'id': 1, 'name': None} )
@main_blueprint.route('/menu/s/',defaults={'name':'General','id' : None })
@main_blueprint.route('/menu/s/<string:name>',defaults={'name':'General','id' : None })
def menu_page(id=None,name=None):

    # Get the menu
    if(id):
        menu = Menu.query.get(id)
    if(name):
        menu = Menu.query.filter(Menu.name==name).first()
    if(not(id) and not(name)):
        id = 1
        menu = Menu.query.get(id)

    # Now get the items with this particular menu
    itemsInMenu = MenuItems.query.filter(MenuItems.menu_id==menu.id).all()
    menuItems = list()
    for item in itemsInMenu:
        menuItems.append(MenuItem.query.get(item.item_id))

    return render_template('main/menu_page.html', menuItems=menuItems)


# The User page is accessible to authenticated users (users that have logged in)
@main_blueprint.route('/edit/menu')
@login_required  # Limits access to authenticated users
def member_page():
    return render_template('main/user_page.html')


# The Admin page is accessible to users with the 'admin' role
@main_blueprint.route('/edit/menu')
@roles_required('admin')  # Limits access to users with the 'admin' role
def admin_page():
    return render_template('main/admin_page.html')

@main_blueprint.route('/main/profile', methods=['GET', 'POST'])
@login_required
def user_profile_page():
    # Initialize form
    form = UserProfileForm(request.form, obj=current_user)

    # Process valid POST
    if request.method == 'POST' and form.validate():
        # Copy form fields to user_profile fields
        form.populate_obj(current_user)

        # Save user_profile
        db.session.commit()

        # Redirect to home page
        return redirect(url_for('main.menu_page'))

    # Process GET or invalid POST
    return render_template('main/user_profile_page.html',
                           form=form)
