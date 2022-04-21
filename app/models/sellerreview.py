from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash
from .. import login
import datetime


class SellerReview():
    def __init__(self, buyer_id, seller_name, seller_id, review_date, rating, description):
        self.buyer_id = buyer_id
        self.seller_name = seller_name
        self.seller_id = seller_id
        self.review_date = review_date
        self.rating = rating
        self.description = description
        
    @staticmethod
    def get_all():
        rows = app.db.execute("""
        SELECT buyer_id, name, seller_id, review_date, rating, description   
        FROM SellerReviews
        INNER JOIN Users
        ON SellerReviews.buyer_id = Users.id
        ORDER BY review_date DESC, rating DESC
        LIMIT 10
        """)
        return [] if not rows else [SellerReview(*row) for row in rows]

    @staticmethod
    def new_sr(buyer_id, seller_id, rating, description):
        try:
            rows = app.db.execute("""
            INSERT INTO SellerReviews(buyer_id, seller_id, review_date, rating, description)
            VALUES(:buyer_id, :seller_id, :review_date, :rating, :description)
            """,
            buyer_id=buyer_id,
            seller_id=seller_id,
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
    def get_all_reviews_by_buyer(buyer_id):
        rows = app.db.execute("""
        SELECT buyer_id, name, seller_id, review_date, rating, description 
        FROM SellerReviews INNER JOIN Users ON SellerReviews.seller_id = Users.id
        WHERE buyer_id = :buyer_id
        ORDER BY review_date DESC
        """,
        buyer_id=buyer_id)
        return [] if not rows else [SellerReview(*row) for row in rows]
    
    @staticmethod
    def get_all_reviews_for_seller(seller_id):
        rows = app.db.execute("""
        SELECT buyer_id, name, seller_id, review_date, rating, description 
        FROM SellerReviews INNER JOIN Users ON SellerReviews.seller_id = Users.id
        WHERE seller_id = :seller_id
        ORDER BY review_date DESC
        """,
        seller_id=seller_id)
        return None if not rows else [SellerReview(*row) for row in rows]
    
    @staticmethod
    def get_all_reviews_at_rating(rating):
        rows = app.db.execute("""
        SELECT *
        FROM SellerReviews
        WHERE rating = :rating
        """,
        rating=rating)
        return None if not rows else [SellerReview(*row) for row in rows]

    @staticmethod
    def get_all_reviews_at_rating_for_seller(seller_id, rating):
        rows = app.db.execute("""
        SELECT *
        FROM SellerReviews
        WHERE seller_id = :seller_id
        AND rating = :rating
        """,
        seller_id=seller_id,
        rating=rating)
        return None if not rows else [SellerReview(*row) for row in rows]

    @staticmethod
    def delete(buyer_id, seller_id):
        app.db.execute_with_no_return("""
        DELETE FROM SellerReviews
        WHERE buyer_id = :buyer_id
        AND seller_id = :seller_id
        """,
        buyer_id=buyer_id, seller_id=seller_id)
