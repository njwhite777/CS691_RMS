from app.models.menuItem_models import Menu, MenuItem, MenuItems


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
