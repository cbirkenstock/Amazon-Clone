from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DecimalField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_babel import _, lazy_gettext as _l

from .models.product import Product
from .models.orderedItem import OrderedItem


from flask import Blueprint
bp = Blueprint('sellerDashboard', __name__)

class AddProductForm(FlaskForm):
    name = StringField(_l('Name'), validators=[DataRequired()])
    quantity = StringField(_l('Quantity'), validators=[DataRequired()])
    category = StringField(_l('Category'), validators=[DataRequired()])
    description = StringField(_l('Description'), validators=[DataRequired()])
    price = DecimalField(_l('Price'), validators=[DataRequired()])
    available = BooleanField(_l('Available'), validators=[DataRequired()])
    image = StringField(_l('Image'), validators=[DataRequired()])
    submit = SubmitField(_l('Add Product'))

@bp.route('/goToInventory/<int:edit>', methods=['GET', 'POST'])
def goToDashboard(edit):   
    # find the products current user has for sale:
    user = current_user._get_current_object()
    user_id = user.id
    #print(OrderedItem.get_purchase_history(user_id)) 
    inventory = Product.get_all_byseller(10, 0, user_id)
    orders = OrderedItem.get_all_for_seller(True, False, user_id)
    topFiveProductsAndData = OrderedItem.get_most_popular_items(user_id);
    form = AddProductForm()

    q = ""
    q = request.args.get('q')
    if q == None:
        q = ''

    if q != "":
        inventory = Product.get_name(15, 0, q)

    o = ""
    o = request.args.get('o')
    if o == None:
        o = ''

    if o != "":
        orders = OrderedItem.get_name(15, 0, o, user_id)

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

    if edit == 0:
        return render_template('sellerDashboard.html', inventory = inventory, orders = orders, editing=False, HTMLData=HTMLData, HTMLData2=HTMLData2, form=form, personal=topFiveProductsAndData[3]) 
    else: 
        return render_template('sellerDashboard.html', inventory = inventory, orders = orders, editing=True, HTMLData=HTMLData, HTMLData2=HTMLData2, form=form) 

'''
class PurchasesForm(FlaskForm):

    @bp.route('/profile', methods=['GET', 'POST'])
    
    def profile():
        #now = datetime.now()
        q = ""
        order= "DESC"
        q = request.args.get('q')
        order = request.args.get('order')
        if q == None:
            q = ''
        if order == None:
            order = 'DESC'
        
        orders_id = []

        #for oid in Purchase.get_all_oids(current_user.id):
            #orders_id.append(oid)
        

        if q == "" and order == "DESC":
            product_info = Purchase.get_all_by_uid_since(current_user.id)
            #product_info = Purchase.get_all_by_nothing()
            

            #q = '9'
            #product_info = Purchase.get_products(q)
            

        elif q == "" and order == "ASC":
            product_info = Purchase.get_all_by_uid_since_ASC(current_user.id)
            #product_info = Purchase.get_all_by_nothing_ASC()
            

        elif order == "DESC":
            product_info = Purchase.get_order_id(current_user.id,q)
            #product_info = Purchase.get_nothing_order_id(q)
            
        else:
            product_info = Purchase.get_order_id_ASC(current_user.id,q)
            #product_info = Purchase.get_nothing_order_id_ASC(q)
        

        form = PurchasesForm()
       
        return render_template('profile.html',
                            purchased_products=product_info,
                            form=form)
'''

@bp.route('/addProduct', methods=['GET', 'POST'])
def addProduct():    
    form = AddProductForm()
    user = current_user._get_current_object()
    user_id = user.id
    if form.validate_on_submit():
        if Product.addProduct(user_id, form.name.data, form.quantity.data, 
            form.category.data, form.description.data, 
            form.price.data, form.available.data, 
            form.image.data):
                #flash('Product Added!')
                return redirect(url_for('sellerDashboard.goToDashboard', edit=0))
    return render_template('addProduct.html', form = form) 


@bp.route('/makeProductUnavailable/<int:id>', methods=['GET', 'POST'])
def makeProductUnavailable(id):    
    Product.makeProductUnavailable(id);
    return redirect(url_for('sellerDashboard.goToDashboard', edit=1));
    #return redirect(url_for('sellerDashboard.goToDashboard'))

@bp.route('/goToInventory/updateProduct/<int:id>/<int:quantity>', methods=['GET', 'POST'])
def updateProduct(id, quantity):   
    Product.updateProduct(id, quantity);
    return redirect(url_for('sellerDashboard.goToDashboard', edit=0));

@bp.route('/fulfillOrder/<int:order_id>/<int:product_id>', methods=['GET', 'POST'])
def fulfillOrder(order_id, product_id):   
    OrderedItem.fulfillOrder(order_id, product_id);
    return redirect(url_for('sellerDashboard.goToDashboard', edit=0));

