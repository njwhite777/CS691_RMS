from app.models.menuItem_models import Menu, MenuItem, MenuItems
from app.models.restaurant_models import Restaurant, RestaurantMenus, RestaurantEmployees
from app.models.employee_models import Employee,EmployeeRoles,Role
from app.models.category_models import ItemCategory,Category,MenuCategories
from app.models.order_models import Order,OrderItems,OrderAssignments
from sqlalchemy import and_, or_,func
from sqlalchemy.sql import label
from app import db




def getMenuItems(id=None,name=None):

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
    return menuItems

def getRestaurants():
    return Restaurant.query.filter().all()

def getRestaurantOrders():
    restaurantOrders = db.session.query(Order.restaurant_id).distinct()
    print(restaurantOrders)
    if(restaurantOrders):
        return [ Restaurant.query.get(o.restaurant_id) for o in restaurantOrders ]
    else:
        return []

def getEmployees():
    return Employee.query.filter().all()


def getMenus():
    return Menu.query.filter().all()


def getItems():
    return MenuItem.query.filter().all()

def getOrderByID(order_id):
    return Order.query.get(order_id)

def getRestaurantByName(name):
    return Restaurant.query.filter(Restaurant.name==name).first()

def getCategorizedMenuItems(menu_id):
    q = db.session.query(Menu,MenuItems,MenuItem,ItemCategory,Category).filter(Menu.id==menu_id).join(MenuItems).join(MenuItem).join(ItemCategory).join(Category)
    r=db.session.execute(q)
    data = list()
    for row in r:
        t = {
            'menu_name': row['menu_name'],
            'item_name': row['menu_item_name'],
            'item_price': row['menu_item_price'],
            'item_information': row['menu_item_information'],
            'item_allergy_information': row['menu_item_allergy_information'],
            'item_ingredients': row['menu_item_ingredients'],
            'item_id' : row['menu_items_item_id'],
            'menu_item_id': row['menu_item_id'],
            'category_name': row['category_name']
        }
        data.append(t)
    return data

def generateOrderReportForInterval(startDate,stopDate,when=None):
    data = dict()
    if(when):
        data['when'] = when

    data['start_date'] = startDate.strftime("%b %d, %Y")
    data['stop_date'] =  stopDate.strftime("%b %d, %Y")

    orders = Order.query.filter(and_(*[Order.order_placed>startDate,Order.order_placed<stopDate,Order.order_status>0])).all()
    restaurant_breakdown = db.session.query(Order,Restaurant,OrderItems,MenuItem,label('total_value',func.sum(MenuItem.price))).filter(and_(*[Order.order_placed>startDate,Order.order_placed<stopDate,Order.order_status>0])).join(Restaurant).join(OrderItems).join(MenuItem).group_by(Restaurant.id).all()
    restaurant_item_counts = db.session.query(Order,Restaurant,OrderItems,MenuItem,label('item_count',func.count(MenuItem.id))).filter(and_(*[Order.order_placed>startDate,Order.order_placed<stopDate,Order.order_status>0])).join(Restaurant).join(OrderItems).join(MenuItem).group_by(Restaurant.id,MenuItem.id).all()
    data['restaurants'] = restaurant_breakdown
    data['ric'] = restaurant_item_counts
    gv = 0
    for i in orders:
        for oi in i.items:
            gv += int(oi.price)
    data['total_value'] = gv
    data['total_ordered'] = len(orders)
    return data

def generateEmployeeReportForInterval(startDate,stopDate,when=None):
    data = dict()
    if(when):
        # Its not if, but when.
        data['when'] = when

    data['start_date'] = startDate.strftime("%b %d, %Y")
    data['stop_date'] =  stopDate.strftime("%b %d, %Y")

    total_employees = db.session.query(Employee,func.count(Employee.id)).first()
    data['total_employees'] = total_employees[1]
    data['roles'] = db.session.query(Employee,EmployeeRoles,Role,label('count',func.count(Employee.id))).join(EmployeeRoles).join(Role).group_by(Role.name).distinct(Employee.id).all()

    data['order_stats'] = db.session.query(Employee,OrderAssignments,Order,Restaurant,label('service_count',func.count(Order.id))).filter(and_(*[Order.order_placed>startDate,Order.order_placed<stopDate,Order.order_status>1])).join(OrderAssignments).join(Order).join(Restaurant).group_by(Restaurant.id,Employee.id).all()

    return data
