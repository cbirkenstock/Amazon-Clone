from sqlalchemy.sql.elements import Null
from .models.cartentries import CartEntry
from .models.purchase import Purchase
from flask_login import current_user
from flask import render_template, redirect, url_for, request
from flask import Blueprint
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired, NumberRange
from flask_babel import _, lazy_gettext as _l

bp = Blueprint('checkout', __name__)

class AddrForm(FlaskForm):
    address = StringField(_l('Address:'), validators=[DataRequired()])
    submit = SubmitField(_l('Confirm Address and Submit Order'))


@bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    form = AddrForm()
    if current_user.is_authenticated:
        CartEntry.checkInventory(current_user.id)
        fullcart = CartEntry.get_user_cart(current_user.id)
        price = CartEntry.getFullPrice(current_user.id)
    
        if form.validate_on_submit():
            address = form.address.data
            check = Purchase.logOrder(current_user.id, CartEntry.getFullPrice(current_user.id), CartEntry.getNumItems(current_user.id), address)
            if check is None or check is False:
                return(redirect(url_for('checkout.checkout')))
            else:
                return(redirect(url_for('order.order', order_id = check)))
        
        return render_template('checkout.html', user_cart = fullcart, price = price, form = form, bal = round(current_user.balance, 2))
    else:
        return(redirect(url_for('users.login')))