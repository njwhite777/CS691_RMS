from app.models.menuItem_models import Menu, MenuItem, MenuItems
from app.models.restaurant_models import Restaurant, RestaurantMenus, RestaurantEmployees
from app.models.employee_models import Employee


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

def getEmployees():
    return Employee.query.filter().all()


def getMenus():
    return Menu.query.filter().all()


def getItems():
    return MenuItem.query.filter().all()
