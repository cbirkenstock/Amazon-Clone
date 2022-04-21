from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_babel import _, lazy_gettext as _l

from .models.product import Product
from .models.orderedItem import OrderedItem


from flask import Blueprint
bp = Blueprint('sellerDashboard', __name__)
def __init__(self, product_id, seller_id, name, quantity, category, description, price, available, image):

class AddProductForm(FlaskForm):
    name = StringField(_l('Name'), validators=[DataRequired()])
    quantity = StringField(_l('Quantity'), validators=[DataRequired()])
    category = StringField(_l('Dategory'), validators=[DataRequired()])
    description = StringField(_l('Description'), validators=[DataRequired()])
    price = IntegerField(_l('Price'), validators=[DataRequired()])
    available = BooleanField(_l('Available'), validators=[DataRequired()])
    image = StringField(_l('Image'), validators=[DataRequired()])

@bp.route('/goToInventory', methods=['GET', 'POST'])
def goToDashboard():    
    # find the products current user has for sale:
    user = current_user._get_current_object()
    user_id = user.id
    #inventory = Product.get_all_byseller(True, user_id)
    inventory = Product.get_all(True)
    orders = OrderedItem.get_all(True, False)
    topFiveProductsAndData = OrderedItem.get_most_popular_items();
    


    HTMLData = [["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]]
    HTMLData2 = topFiveProductsAndData[2]

    names = topFiveProductsAndData[0]
    data = topFiveProductsAndData[1]
    

    for name in names: 
        tempData = [0 for i in range(12)] 
        for i in range(0,5):
            tempName = names[i]
        for point in data: 
            if point[0]==name:
                tempData[(int(point[2]) - 1)] = point[1]
        HTMLData.append([name, tempData])          

    return render_template('sellerDashboard.html', inventory = inventory, orders = orders, editing=False, HTMLData=HTMLData, HTMLData2=HTMLData2 ) 
    
