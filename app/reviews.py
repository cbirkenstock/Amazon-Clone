from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
import datetime
from .models.product import Product
from .models.purchase import Purchase
from .models.productreview import ProductReview
from .models.sellerreview import SellerReview
from flask import Blueprint, request
from flask import current_app as app
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, BooleanField, SubmitField, validators
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_babel import _, lazy_gettext as _l


bp = Blueprint('reviews', __name__)

@bp.route('/reviews')
def load():
    categories = ['Product Reviews', 'Seller Reviews']
    category = request.args.get('categories')
    colnames = ['Product', 'Customer ID', 'Rating', 'Description', 'Date', 'Edit', 'Delete']
    if category == 'Seller Reviews':
        colnames[0] = 'Seller'
    if category == None:
        category = 'Product Reviews'
    if current_user.is_authenticated:
        user = current_user._get_current_object()
        user_id = current_user.id
        Reviews = ProductReview.get_all_reviews_by_user(user_id)
        Reviews2 = SellerReview.get_all_reviews_by_buyer(user_id)
    else:
        Reviews = ProductReview.get_all()
        Reviews2 = SellerReview.get_all()
    return render_template('reviews.html', Reviews=Reviews, Reviews2=Reviews2, categories=categories, colnames=colnames)

class NewProductReview(FlaskForm):
    product = StringField(_l('Product'), validators=[DataRequired()])
    rating = IntegerField(_l('Rating (0-5)'), validators=[DataRequired()])
    description = StringField(_l('Description'))
    submit = SubmitField(_l('Submit'))

    def validate_product(self, product):
        rows = app.db.execute('''
        SELECT product_id
        FROM Products
        WHERE name = :product
        ''',
        product=product.data)
        if not rows:
            raise ValidationError(_('Product does not exist.'))

    def validate_rating(self, rating):
        if not (1 <= rating.data <= 5):
            raise ValidationError(_('Rating must be between 1 and 5.'))


@bp.route('/reviews/newPR', methods=['GET', 'POST'])
def newPR():
    form = NewProductReview()
    user = current_user._get_current_object()
    if current_user.is_authenticated:
        user_id = user.id
    else:
        return redirect(url_for('users.login'))
    if form.validate_on_submit():
        product_id = app.db.execute("""SELECT product_id FROM Products WHERE name = :bob""", bob=form.product.data)[0][0]
        if ProductReview.new_pr(user_id, product_id, form.rating.data, form.description.data):
            flash('Review Submitted!')
            return redirect(url_for('reviews.load'))
        else:
            return redirect(url_for('reviews.load'))
    return render_template('newPR.html', form=form)

class NewSellerReview(FlaskForm):
    seller = StringField(_l('Seller'), validators=[DataRequired()])
    rating = IntegerField(_l('Rating (0-5)'), validators=[DataRequired()])
    description = StringField(_l('Description'))
    submit = SubmitField(_l('Submit'))
    def validate_seller(self, seller):
        rows = app.db.execute('''
        SELECT Sellers.id
        FROM Users INNER JOIN Sellers ON Users.id=Sellers.id
        WHERE Users.name = :seller
        ''',
        seller=seller.data)
        if not rows:
            raise ValidationError(_('Seller does not exist.'))
    def validate_rating(self, rating):
        if not (1 <= rating.data <= 5):
            raise ValidationError(_('Rating must be between 1 and 5.'))

@bp.route('/reviews/newSR', methods=['GET', 'POST'])
def newSR():
    if current_user.is_authenticated == False:
        return redirect(url_for('users.login'))
    form = NewSellerReview()
    user = current_user._get_current_object()
    buyer_id = user.id
    if form.validate_on_submit():
        seller_id = app.db.execute("""SELECT id FROM Users WHERE name = :bob""", bob=form.seller.data)[0][0]
        if SellerReview.new_sr(buyer_id, seller_id, form.rating.data, form.description.data):
            flash('Review Submitted!')
            return redirect(url_for('reviews.load'))
        else:
            return redirect(url_for('reviews.load'))
    return render_template('newSR.html', form=form)

@bp.route('/reviews/deleteSR/<int:buyer_id>/<int:seller_id>', methods=['GET', 'POST'])
def deleteSR(buyer_id, seller_id): 
    SellerReview.delete(buyer_id, seller_id)
    return redirect(url_for('reviews.load'))

@bp.route('/reviews/deletePR/<int:user_id>/<int:product_id>', methods=['GET', 'POST'])
def deletePR(user_id, product_id):
    ProductReview.delete(user_id, product_id)
    return redirect(url_for('reviews.load'))

class EditReview(FlaskForm):
    rating = IntegerField(_l('Rating (0-5)'), validators=[DataRequired()])
    description = StringField(_l('Description'))
    submit = SubmitField(_l('Submit'))
    def validate_rating(self, rating):
        if not (1 <= rating.data <= 5):
            raise ValidationError(_('Rating must be between 1 and 5.'))

@bp.route('/reviews/editPR/<int:user_id>/<int:product_id>', methods=['GET', 'POST'])
def editPR(user_id, product_id):
    ProductReview.delete(user_id, product_id)
    form = EditReview()
    product_name = app.db.execute("""SELECT name FROM Products WHERE product_id = :product_id""", product_id=product_id)[0][0]
    user_name = app.db.execute("""SELECT name FROM Users WHERE id = :user_id""", user_id=user_id)[0][0]
    if form.validate_on_submit():
        if ProductReview.new_pr(user_id, product_id, form.rating.data, form.description.data):
            flash('Review Updated!')
            return redirect(url_for('reviews.load'))
        else:
            return redirect(url_for('reviews.load'))
    return render_template('editPR.html', form=form, user_name=user_name, product_name=product_name)

@bp.route('/reviews/editSR/<int:buyer_id>/<int:seller_id>', methods=['GET', 'POST'])
def editSR(buyer_id, seller_id):
    SellerReview.delete(buyer_id, seller_id)
    form = EditReview()
    seller_name = app.db.execute("""SELECT name FROM Users WHERE id = :seller_id""", seller_id=seller_id)[0][0]
    buyer_name = app.db.execute("""SELECT name FROM Users WHERE id = :buyer_id""", buyer_id=buyer_id)[0][0]
    if form.validate_on_submit():
        if SellerReview.new_sr(buyer_id, seller_id, form.rating.data, form.description.data):
            flash('Review Updated!')

@bp.route('/reviews/ss/<int:seller_id>', methods=['GET', 'POST'])
def sellerSummary(seller_id):
    seller_name = app.db.execute("""SELECT name from Users WHERE id = :seller_id""", seller_id=seller_id)[0][0]
    num_ratings = app.db.execute("""SELECT COUNT(rating) from SellerReviews WHERE seller_id = :seller_id""", seller_id=seller_id)[0][0]
    avg_ratings = app.db.execute("""SELECT AVG(rating) from SellerReviews WHERE seller_id = :seller_id""", seller_id=seller_id)[0][0]
    recent_reviews = SellerReview.get_all_reviews_for_seller(seller_id)
    if not recent_reviews:
        recent_reviews = []
    return render_template('sellerSummary.html', seller_id=seller_id, seller_name=seller_name, num_ratings=num_ratings, avg_ratings=avg_ratings, recent_reviews=recent_reviews)

@bp.route('/reviews/ps/<int:product_id>', methods=['GET', 'POST'])
def productSummary(product_id):
    product_name = app.db.execute("""SELECT name from Products WHERE product_id = :product_id""", product_id=product_id)[0][0]
    num_ratings = app.db.execute("""SELECT COUNT(rating) from ProductReviews WHERE product_id = :product_id""", product_id=product_id)[0][0]
    avg_ratings = app.db.execute("""SELECT AVG(rating) from ProductReviews WHERE product_id = :product_id""", product_id=product_id)[0][0]
    recent_reviews = ProductReview.get_all_reviews_for_product(product_id)
    if not recent_reviews:
        recent_reviews = []
    return render_template('productSummary.html', product_name=product_name, num_ratings=num_ratings, avg_ratings=avg_ratings, recent_reviews=recent_reviews)
