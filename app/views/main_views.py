# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>


from flask import Blueprint, redirect, render_template
from flask import request, url_for
from flask_user import current_user, login_required, roles_required

from app import db
from app.models.user_models import UserProfileForm
from app.models.menuItem_models import Menu, MenuItem, MenuItems
from .view_helpers import *

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
@main_blueprint.route('/menu/<int:id>' )
@main_blueprint.route('/menu/s/')
@main_blueprint.route('/menu/s/<string:name>')
def menu_page(id=None,name=None):
    menuItems = getMenuItems(id,name)
    return render_template('main/menu_page.html', menuItems=menuItems,editable=False)


# The User page is accessible to authenticated users (users that have logged in)
@main_blueprint.route('/edit/menu')
@main_blueprint.route('/edit/menu/<int:id>')
@main_blueprint.route('/edit/menu/s/')
@main_blueprint.route('/edit/menu/s/<string:name>')
@login_required  # Limits access to authenticated users
def edit_menu_page(id=None,name=None):
    menuItems = getMenuItems(id,name)
    isAdmin = current_user.has_roles('admin')
    return render_template('main/menu_page.html',menuItems=menuItems,editable=True)


# The Admin page is accessible to users with the 'admin' role
@main_blueprint.route('/edit/site')
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
