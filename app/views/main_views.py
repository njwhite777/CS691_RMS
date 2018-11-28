# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>


from flask import Blueprint, redirect, render_template
from flask import request, url_for
from flask_user import current_user, login_required, roles_required

from app import db
from app.models.employee_models import EmployeeProfileForm
from app.models.menuItem_models import Menu, MenuItem, MenuItems
from app.models.order_models import Order,OrderItems,OrderAssignments
from .view_helpers import *

import datetime
from datetime import timezone
import time

main_blueprint = Blueprint('main', __name__, template_folder='templates')

# The Home page is accessible to anyone
@main_blueprint.route('/')
def home_page():
    restaurants = getRestaurants()
    if(len(restaurants)>0):
        r = restaurants[0]
        return redirect("/"+ r.name+"/menu")
    return redirect('/restaurants')

@main_blueprint.route('/restaurants')
def restaurant_lading():
    restaurants = getRestaurants()
    return render_template('restaurant/restaurants.html',restaurants=restaurants)

# The Home page is accessible to anyone
@main_blueprint.route('/_users')
def users_page():
    return render_template('main/_users.html')

# The User page is accessible to authenticated users (users that have logged in)
@main_blueprint.route('/<string:name>/menu')
def restaurant_menu_page(name=None):
    r = getRestaurantByName(name)
    v = getCategorizedMenuItems(r.getMenu().id)
    categories = [ i['category_name'] for i in v ]
    return render_template('restaurant/menu.html',restaurant=r,title="Menu for " + name,categorizedItems=v,categories=categories)

@main_blueprint.route('/<string:name>/order/<int:order_id>')
def restaurant_order_status(name=None,order_id=None):
    if(order_id == None or name == None):
        return
    order = getOrderByID(order_id)
    restaurant = getRestaurantByName(name)
    ordertime = order.order_placed.replace(tzinfo=timezone.utc).astimezone(tz=None)
    return render_template('restaurant/order_status.html',title="Order Status ",purpose="Order Status",order=order,restaurant=restaurant,ordertime=ordertime)

@main_blueprint.route('/manage/employee/report')
@login_required
@roles_required('owner')  # Limits access to users with the 'owner' role
def get_employee_report():
    today = datetime.datetime.utcnow()
    report = dict()
    lreport = dict()
    reports=list()
    startDate = today - datetime.timedelta(days=today.weekday())
    endDate = startDate + datetime.timedelta(days=6)
    lstartDate = startDate - datetime.timedelta(days=7)
    lendDate = startDate - datetime.timedelta(days=1)

    reports = reports + [generateEmployeeReportForInterval(startDate,endDate,'This Week: ')] + [generateEmployeeReportForInterval(lstartDate,lendDate,'Last Week: ')]
    return render_template('main/employee_report.html',purpose="Report on Employees",title="Menu Managment",reports=reports)

@main_blueprint.route('/manage/order/report')
@login_required
@roles_required('owner')  # Limits access to users with the 'owner' role
def get_order_report():
    today = datetime.datetime.utcnow()
    report = dict()
    lreport = dict()
    reports=list()
    startDate = today - datetime.timedelta(days=today.weekday())
    endDate = startDate + datetime.timedelta(days=6)
    lstartDate = startDate - datetime.timedelta(days=7)
    lendDate = startDate - datetime.timedelta(days=1)
    reports = reports + [generateOrderReportForInterval(startDate,endDate,'This Week: ')] + [generateOrderReportForInterval(lstartDate,lendDate,'Last Week: ')]
    return render_template('main/order_report.html',purpose="Report on Restaurant Orders",title="Report on Orders",reports=reports)

# The User page is accessible to authenticated users (users that have logged in)
@main_blueprint.route('/manage/menu')
@login_required
@roles_required('owner')  # Limits access to users with the 'owner' role
def add_menu_page():
    menus = getMenus()
    menuItems = getItems()
    return render_template('menu/add_menu_page.html',purpose="Menu Mangment",title="Menu Managment",menus=menus,menuItems=menuItems)

@main_blueprint.route('/manage/menuitems')
@login_required
def menu_item_manager():
    menuItems = getItems()
    isOwner = current_user.has_roles('owner')
    return render_template('menuitem/menu_page.html',purpose="Menu Item Managment",title="Item Managment",menuItems=menuItems,editable=True,isOwner=isOwner)

@main_blueprint.route('/manage/orders')
@login_required
def order_managment():
    restaurants_with_orders = getRestaurantOrders()
    return render_template('restaurant/orders.html',purpose="Order Managment",title="Order Managment",restaurants_with_orders=restaurants_with_orders,timezone=timezone)

@main_blueprint.route('/manage/restaurant')
@login_required
@roles_required('owner')  # Limits access to users with the 'owner' role
def restaurant_manager():
    restaurants = getRestaurants()
    employees = getEmployees()
    menus = getMenus()
    return render_template('restaurant/restaurant_page.html',purpose="Restaurant Mangment",title="Restaurant Managment",restaurants=restaurants,employees=employees,menus=menus)

@main_blueprint.route('/edit/menu/<int:id>')
@main_blueprint.route('/edit/menu/s/<string:name>')
@login_required  # Limits access to authenticated users
@roles_required(['owner','waiter'])  # Limits access to users with the 'owner' role
def edit_menu_page(id=None,name=None):
    menuItems = getMenuItems(id,name)
    isOwner = current_user.has_roles('owner')
    isWaiter = current_user.has_roles('waiter')
    return render_template('menu/menu_page.html',title="Edit Menu",menuItems=menuItems,editable=True,isOwner=isOwner,isWaiter=isWaiter)

# The Admin page is accessible to users with the 'owner' role
@main_blueprint.route('/edit/site')
@roles_required('owner')  # Limits access to users with the 'owner' role
def admin_page():
    return render_template('main/admin_page.html')

@main_blueprint.route('/main/profile', methods=['GET', 'POST'])
@login_required
def user_profile_page():
    # Initialize form
    form = EmployeeProfileForm(request.form, obj=current_user)

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
