# from flask_user import UserMixin
# from flask_user.forms import RegisterForm
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators
from app import db
from app.models.employee_models import Employee

class Restaurant(db.Model):
    __tablename__ = 'restaurant'
    # Restaurant id
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(255), nullable=False, server_default='')
    picture_url = db.Column(db.String(255), nullable=False, server_default='')
    tagline  = db.Column(db.String(255), nullable=False, server_default='')

    def getEmployees(self):
        res = RestaurantEmployees.query.filter(RestaurantEmployees.restaurant_id==self.id).all()
        employees = list()
        for employee in res:
            e = Employee.query.filter(Employee.id==employee.employee_id).first()
            if(e):
                employees.append(e)
        return employees

    def getEmployeeIds(self):
        return [ e.id for e in self.getEmployees() ]

    def getMenu(self):
        return RestaurantMenus.query.filter(RestaurantMenus.restaurant_id==self.id).first()

    def getMenuID(self):
        m =  self.getMenu()
        if(m):
            print("RID is ",self.id,"MENU ID: ",m.menu_id)
            return m.menu_id
        return 0

    def toDict(self):
        res = RestaurantEmployees.query.filter(RestaurantEmployees.restaurant_id==self.id).all()
        employees = list()
        for employee in res:
            e = Employee.query.filter(Employee.id==employee.employee_id).first()
            if(e):
                employees.append(e.toDict())

        return {
            'id' : self.id,
            'name': self.name,
            'picture_url': self.picture_url,
            'tagline': self.tagline,
            'employees': employees
        }

class RestaurantMenus(db.Model):
    __tablename__ = 'restaurant_menus'
    id = db.Column(db.Integer(), primary_key=True)
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id', ondelete='CASCADE'))
    restaurant_id = db.Column(db.Integer,db.ForeignKey('restaurant.id', ondelete='CASCADE'))

    def toDict(self):
        return {
            'id' : self.id,
            'menu_id': self.menu_id,
            'restaurant_id': self.restaurant_id
        }

class RestaurantEmployees(db.Model):
    __tablename__ = 'restaurant_employee'
    id = db.Column(db.Integer(), primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id', ondelete='CASCADE'))
    restaurant_id = db.Column(db.Integer,db.ForeignKey('restaurant.id', ondelete='CASCADE'))

    def toDict(self):
        return {
            'id' : self.id,
            'employee_id': self.employee_id,
            'restaurant_id': self.restaurant_id
        }
