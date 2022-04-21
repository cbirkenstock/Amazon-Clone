from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash
from .. import login
import datetime

class ProductReview():
    def __init__(self, user_id, product_name, product_id, review_date, rating, description):
        self.user_id = user_id
        self.product_name = product_name
        self.product_id = product_id
        self.review_date = review_date
        self.rating = rating
        self.description = description

    @staticmethod
    def get_all():
        rows = app.db.execute("""
        SELECT  user_id, name, Products.product_id, review_date, rating, ProductReviews.description
        FROM ProductReviews
        INNER JOIN Products
        ON ProductReviews.product_id = Products.product_id
        ORDER BY review_date DESC, rating DESC
        LIMIT 10
        """)
        return [] if not rows else [ProductReview(*row) for row in rows]
    
    @staticmethod
    def new_pr(user_id, product_id, rating, description):
        try:
            rows = app.db.execute("""
            INSERT INTO ProductReviews(user_id, product_id, review_date, rating, description)
            VALUES(:user_id, :product_id, :review_date, :rating, :description)
            """,
            user_id=user_id,
            product_id=product_id,
            review_date=datetime.datetime.now(),
            rating=rating,
            description=description)   
            return rows

        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            return None

    @staticmethod
    def product_exists(product_id):
        rows = app.db.execute("""
        SELECT *
        FROM Products
        WHERE product_id = :product_id
        """,
        product_id=product_id)
        return len(rows) > 0

    @staticmethod
    def get_all_reviews_by_user(user_id):
        rows = app.db.execute("""
        SELECT user_id, name, Products.product_id, review_date, rating, ProductReviews.description
        FROM ProductReviews INNER JOIN Products ON ProductReviews.product_id = Products.product_id
        WHERE user_id = :user_id
        ORDER BY review_date DESC
        """,
        user_id=user_id)
        return [] if not rows else [ProductReview(*row) for row in rows]
    
    @staticmethod
    def get_all_reviews_for_product(product_id):
        rows = app.db.execute("""
        SELECT user_id, name, Products.product_id, review_date, rating, ProductReviews.description
        FROM ProductReviews INNER JOIN Products ON ProductReviews.product_id = Products.product_id
        WHERE Products.product_id = :product_id
        ORDER BY review_date DESC
        """,
        product_id=product_id)
        return None if not rows else [ProductReview(*row) for row in rows]

    @staticmethod
    def get_all_reviews_for_name(name):
        rows = app.db.execute("""
        SELECT user_id, name, Products.product_id, review_date, rating, ProductReviews.description
        FROM ProductReviews INNER JOIN Products ON ProductReviews.product_id = Products.product_id
        WHERE name = :name
        """,
        name=name)
        return [] if not rows else [ProductReview(*row) for row in rows]

    @staticmethod
    def get_all_reviews_at_rating(rating):
        rows = app.db.execute("""
        SELECT *
        FROM ProductReviews
        WHERE rating = :rating
        """,
        rating=rating)
        return None if not rows else [ProductReview(*row) for row in rows]

    @staticmethod
    def get_all_reviews_at_rating_for_product(product_id, rating):
        rows = app.db.execute("""
        SELECT *
        FROM ProductReviews
        WHERE product_id = :product_id
        AND rating = :rating
        """,
        product_id=product_id,
        rating=rating)
        return None if not rows else [ProductReview(*row) for row in rows]

    @staticmethod
    def delete(user_id, product_id):
        rows = app.db.execute_with_no_return("""
        DELETE FROM ProductReviews
        WHERE user_id = :user_id
        AND product_id = :product_id
        """,
        user_id=user_id, product_id=product_id)

