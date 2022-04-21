from .models.cartentries import CartEntry
from .models.savedEntries import sflEntry
from flask_login import current_user
from flask import render_template, redirect, url_for
from flask import Blueprint
from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField
from wtforms.validators import DataRequired, NumberRange
from flask_babel import _, lazy_gettext as _l


bp = Blueprint('cart', __name__)

class SaveCart(FlaskForm):
	submit=SubmitField(_l('Save Cart For Later'))

class BackToCart(FlaskForm):
	quantity = IntegerField(_l('Quantity'),validators=[DataRequired(), NumberRange(min=0)])
	submit = SubmitField(_l('Add to Cart'))

@bp.route('/cart', methods=['GET','POST'])
def cart():
	saveForm = SaveCart()
	addBack = BackToCart()
	if current_user.is_authenticated:
		fullcart = CartEntry.get_user_cart(current_user.id)
		saved = sflEntry.get_user_SFL(current_user.id)
		price = CartEntry.getFullPrice(current_user.id)
		return render_template('cart.html', user_cart=fullcart, user_saved=saved, balance=round(current_user.balance, 2), price = price)
		
	else:
		return(redirect(url_for('users.login')))

	

@bp.route('/addBack/<int:product_id>', methods=['GET','POST'])
def addBack(product_id):
	sflEntry.addItemBack(current_user.id, product_id)
	return redirect(url_for('cart.cart'))

@bp.route('/saveCart', methods=['GET','POST'])
def saveCart():
	CartEntry.save_whole_cart(current_user.id)
	return redirect(url_for('cart.cart'))

@bp.route('/saveItem/<int:product_id>', methods=['GET','POST'])
def saveItem(product_id):
	CartEntry.saveItem(current_user.id, product_id)
	return redirect(url_for('cart.cart'))

@bp.route('/deleteItem/<int:product_id>', methods=['GET','POST'])
def delItem(product_id):
	CartEntry.delItem(current_user.id, product_id)
	return redirect(url_for('cart.cart'))

@bp.route('/add1/<int:product_id>', methods=['GET','POST'])
def add1(product_id):
	CartEntry.add1(current_user.id, product_id)
	return redirect(url_for('cart.cart'))

@bp.route('/add5/<int:product_id>', methods=['GET','POST'])
def add5(product_id):
	CartEntry.add5(current_user.id, product_id)
	return redirect(url_for('cart.cart'))

@bp.route('/add10/<int:product_id>', methods=['GET','POST'])
def add10(product_id):
	CartEntry.add10(current_user.id, product_id)
	return redirect(url_for('cart.cart'))

@bp.route('/rem1/<int:product_id>', methods=['GET','POST'])
def rem1(product_id):
	CartEntry.rem1(current_user.id, product_id)
	return redirect(url_for('cart.cart'))

@bp.route('/rem5/<int:product_id>', methods=['GET','POST'])
def rem5(product_id):
	CartEntry.rem5(current_user.id, product_id)
	return redirect(url_for('cart.cart'))

@bp.route('/rem10/<int:product_id>', methods=['GET','POST'])
def rem10(product_id):
	CartEntry.rem10(current_user.id, product_id)
	return redirect(url_for('cart.cart'))

@bp.route('/co-add1/<int:product_id>', methods=['GET','POST'])
def COadd1(product_id):
	CartEntry.add1(current_user.id, product_id)
	return redirect(url_for('checkout.checkout'))

@bp.route('/co-add5/<int:product_id>', methods=['GET','POST'])
def COadd5(product_id):
	CartEntry.add5(current_user.id, product_id)
	return redirect(url_for('checkout.checkout'))

@bp.route('/co-add10/<int:product_id>', methods=['GET','POST'])
def COadd10(product_id):
	CartEntry.add10(current_user.id, product_id)
	return redirect(url_for('checkout.checkout'))

@bp.route('/co-rem1/<int:product_id>', methods=['GET','POST'])
def COrem1(product_id):
	CartEntry.rem1(current_user.id, product_id)
	return redirect(url_for('checkout.checkout'))

@bp.route('/co-rem5/<int:product_id>', methods=['GET','POST'])
def COrem5(product_id):
	CartEntry.rem5(current_user.id, product_id)
	return redirect(url_for('checkout.checkout'))

@bp.route('/co-rem10/<int:product_id>', methods=['GET','POST'])
def COrem10(product_id):
	CartEntry.rem10(current_user.id, product_id)
	return redirect(url_for('checkout.checkout'))

@bp.route('/co-deleteItem/<int:product_id>', methods=['GET','POST'])
def COdelItem(product_id):
	CartEntry.delItem(current_user.id, product_id)
	return redirect(url_for('checkout.checkout'))