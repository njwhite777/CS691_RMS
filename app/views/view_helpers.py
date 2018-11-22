from app.models.menuItem_models import Menu, MenuItem, MenuItems
from app.models.restaurant_models import Restaurant, RestaurantMenus, RestaurantEmployees
from app.models.employee_models import Employee
from app.models.category_models import ItemCategory,Category,MenuCategories

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

def getEmployees():
    return Employee.query.filter().all()


def getMenus():
    return Menu.query.filter().all()


def getItems():
    return MenuItem.query.filter().all()

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
            'menu_item_id': row['menu_item_id'],
            'category_name': row['category_name']
        }
        data.append(t)
    return data
