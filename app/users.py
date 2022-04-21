from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FloatField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Optional
from flask_babel import _, lazy_gettext as _l


from .models.user import User
from .models.sellerreview import SellerReview
from .models.purchase import Purchase
from datetime import datetime



from flask import Blueprint
bp = Blueprint('users', __name__)


'''

# need a link that the cur user would click on that would then take them to selected user
# will need to find seller id or user id from whatever table is being used


class UpdateBalanceForm(FlaskForm):
      
    amount = FloatField(_l('Amount of Money:'), validators=[DataRequired()])
    submitadd = SubmitField(_l('Add to Balance'))
    submitsub = SubmitField(_l('Withdraw from Balance'), validators=[Optional()])

    def validate_amount(self, amount):
       
        if amount.data > 1000000:
            raise ValidationError(_("Cannot add/withdraw over $1,000,000 at a time"))

   
@bp.route('/user_view', methods=['GET', 'POST'])
def display_selected_user():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))

    

    form = DisplaySelectedUser()
    if form.validate_on_submit():
        
            
            return redirect(url_for('users.profile'))
        
        elif form.submitsub.data and form.amount.data > current_user.balance:
            
            flash('Cannot withdraw more than current balance')
            
        
        elif form.submitsub.data and User.sub_balance(formatted_amount):
            
            return redirect(url_for('users.profile'))
        
        

    return render_template('update_balance.html', title='Update Balance', form=form, selected_user=selected_user)
'''







class UpdateBalanceForm(FlaskForm):
      
    amount = FloatField(_l('Amount of Money:'), validators=[DataRequired()])
    submitadd = SubmitField(_l('Add to Balance'))
    submitsub = SubmitField(_l('Withdraw from Balance'), validators=[Optional()])

    def validate_amount(self, amount):
       
        if amount.data > 1000000:
            raise ValidationError(_("Cannot add/withdraw over $1,000,000 at a time"))

   

 
@bp.route('/update_balance', methods=['GET', 'POST'])
def update_balance():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))

    

    form = UpdateBalanceForm()
    if form.validate_on_submit():
        formatted_amount = float("{:.2f}".format(form.amount.data))
        
        if form.submitadd.data and User.add_balance(formatted_amount):
            
            return redirect(url_for('users.profile'))
        
        elif form.submitsub.data and form.amount.data > current_user.balance:
            
            flash('Cannot withdraw more than current balance')
            
        
        elif form.submitsub.data and User.sub_balance(formatted_amount):
            
            return redirect(url_for('users.profile'))
        
        

    return render_template('update_balance.html', title='Update Balance', form=form)


class UpdateProfileForm(FlaskForm):
      
    name = StringField(_l('New Name:'), validators=[Optional()])
    email = StringField(_l('New Email:'), validators=[Optional(), Email()])
    submit = SubmitField(_l('Update Profile'))

    def validate_email(self, email):
        if User.email_exists(email.data):
            raise ValidationError(_("There is already a user with this email"))
 
@bp.route('/update_profile', methods=['GET', 'POST'])
def update_profile():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))


    form = UpdateProfileForm()
    if form.validate_on_submit():
        
        if User.update_profile(form.name.data, form.email.data):
            
            return redirect(url_for('users.profile'))

    return render_template('update_profile.html', title='Update Profile', form=form)

@bp.route('/update_profile_pic', methods=['GET', 'POST'])
def update_profile_pic():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))


    form = UpdateProfileForm()
    if form.validate_on_submit():
        
        if User.update_profile(form.name.data, form.email.data):
            
            return redirect(url_for('users.profile'))

    return render_template('update_profile.html', title='Update Profile', form=form)




class LoginForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Remember Me'))
    submit = SubmitField(_l('Login'))


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_auth(form.email.data, form.password.data)
        if user is None:
            flash("Incorrect email or password")
            return redirect(url_for('users.login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index.index')

        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


class RegistrationForm(FlaskForm):    
    
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _l('Repeat Password'), validators=[DataRequired(),
                                           EqualTo('password')])
    name = StringField(_l('Name'), validators=[DataRequired()])
    submit = SubmitField(_l('Register'))

    def validate_email(self, email):
        if User.email_exists(email.data):
            raise ValidationError(_("There is already a user with this email"))
            

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        
        
        if User.register(form.email.data,
                        form.password.data,
                        form.name.data, 0.00, "tiger"):
            
            user = User.get_by_auth(form.email.data, form.password.data)
            login_user(user)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index.index')

            return redirect(next_page)
            
    return render_template('register.html', title='Register', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index.index'))



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

        #"2014-07-14 05:46:26"
        #

        
 
        # find the products in the selected category:
        product_info = Purchase.get_all_by_uid_since(current_user.id )
        #product_info = Purchase.get_all_by_nothing()
        
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
        
        userorders = Purchase.getUserOrders(current_user.id)
        for n in userorders:
            orderid = n[0]
            Purchase.checkOrderFulfilled(orderid)
       
        return render_template('profile.html',
                            purchased_products=product_info,
                            form=form)



@bp.route('/user_view/<int:user_id>', methods=['GET', 'POST'])
def user_view(user_id):
        
      #  if not current_user.is_authenticated:
           # return redirect(url_for('users.login'))

        user = User.get(user_id)
        
        is_seller = User.is_seller(user_id)
        
        if is_seller:
            reviews = SellerReview.get_all_reviews_for_seller(user_id)
            print(reviews)
        else:
            reviews = None
        if current_user.is_authenticated:
            buttonName = 'Leave a Review'
        else:
            buttonName = 'Login to Leave a Review'
        return render_template('user_view.html',
                                    user=user,
                                    reviews=reviews,
                                    buttonName=buttonName,
                                    is_seller=is_seller)
