from flask import render_template, redirect, url_for
from flask_login import current_user
import datetime

from .models.product import Product
from .models.product import ProductExtended
from .models.purchase import Purchase
from .models.cartentries import CartEntry
from .models.productreview import ProductReview

from flask import request
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, HiddenField
from wtforms.validators import DataRequired, NumberRange
from flask_babel import _, lazy_gettext as _l



from flask import Blueprint
bp = Blueprint('index', __name__)

def helper(page_number, next_page_bool): 
    q = ""
    q = request.args.get('q')
    category = 'All'
    order = 'ASC'
    categories = ['All', 'Clothing', 'Furniture', 'Sports']
    category = request.args.get('categories')
    order = request.args.get('order')
    sortkey = request.args.get('sortkey')
    page_size = 10
    # find the products in the selected category with a description or name that fits the search term: 
    if q == None:
        q = ""
    if category == None:
        category = 'All'
    if order == None:
        order = 'ASC'
    if sortkey == None:
        sortkey = 'None'
    name_products = Product.get_all(page_size, page_number)
    
    if sortkey == 'None':
        if q == "" and category == 'All':
            name_products = Product.get_all(page_size, page_number)
        elif q != "" and category =='All':
            name_products = Product.get_name(page_size, page_number, q)
        elif q == "" and category != 'All': 
            name_products = Product.get_category(page_size, page_number, category)
        else:
            name_products = Product.get_search(page_size, page_number, q, category)

    elif order == 'ASC':
        
        if q == "" and category == 'All':
            name_products = Product.get_all_ASC(page_size, page_number, sortkey)
        elif q != "" and category =='All':
            name_products = Product.get_name_ASC(page_size, page_number, q, sortkey)
        elif q == "" and (category != 'All'):
            name_products = Product.get_category_ASC(page_size, page_number, category, sortkey)
        else:
            name_products = Product.get_search_ASC(page_size, page_number, q, category, sortkey)

    elif order == 'DESC':
        
        if q == "" and category == 'All':
            name_products = Product.get_all_DESC(page_size, page_number, sortkey)
        elif q != "" and category =='All':
            name_products = Product.get_name_DESC(page_size, page_number, q, sortkey)
        elif q == "" and (category != 'All'):
            name_products = Product.get_category_DESC(page_size, page_number, category, sortkey)
        else:
            name_products = Product.get_search_DESC(page_size, page_number, q, category, sortkey)

    else:
        
        name_products = []
    # find the products current user has bought:
    if current_user.is_authenticated:
        buttonName = 'Add to Cart'
    else:
        buttonName = 'Login to Add to Cart'
    if next_page_bool == 1 and name_products == []:
        page_number = page_number-1
        return helper(int(page_number),1)
    else:
        return render_template('index.html',
                           avail_products=name_products,
                           categories=categories,
			   buttonName=buttonName,
			   sortkey=sortkey,
			   first = str(page_size*(page_number)),
                           last = str(page_size*((page_number)+1)),
			   page_number = page_number)

@bp.route('/')
def index():
    return helper(0,0)

@bp.route('/1/<page_number>')
def nextPage(page_number):
    return helper(int(page_number)+1, 1)

@bp.route('/2/<page_number>')
def previousPage(page_number):
    if int(page_number) == 0:
        return helper(int(page_number),0)
    else:
        return helper(int(page_number)-1,0)

@bp.route('/productPage/<name>', methods=['GET', 'POST'])
def productPage(name):
    product = Product.get_all_name(name)
    seller_info = ProductExtended.get_seller_name(name)
    reviews = ProductReview.get_all_reviews_for_name(name)
    if current_user.is_authenticated:
        buttonName = 'Leave a Review'
    else:
        buttonName = 'Login to Leave a Review'
    return render_template('product.html', name = name,
					   seller_info = seller_info,
					   product = product,
					   reviews = reviews,
					   buttonName = buttonName)

@bp.route('/addItem/<int:product_id>', methods=['GET','POST'])
def addItem(product_id):
    if current_user.is_authenticated:
        CartEntry.addItem(current_user.id, product_id)
        return redirect(url_for('index.index'))
    else:
        return redirect(url_for('users.login'))
