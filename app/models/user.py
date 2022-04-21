from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user

from .. import login

 
'''
AUTH METHODS
'''
class User(UserMixin):
    def __init__(self, id, email, name, balance, image):
        self.id = id
        self.email = email
        self.name = name
        self.balance = balance
        self.image = image
         
    @staticmethod
    def get_by_auth(email, password):
        rows = app.db.execute("""
        SELECT password, id, email, name, balance, image
        FROM Users
        WHERE email = :email
        """,
        email=email)
        if not rows:
            return None
        elif not check_password_hash(rows[0][0], password):
            return None
        else:
            return User(*(rows[0][1:]))

    '''
    BALANCE METHODS
    '''
    
    @staticmethod
    def add_balance(amount):
        new_balance = current_user.balance
        if amount != None:
            new_balance = current_user.balance + amount

        rows = app.db.execute("""
        UPDATE Users
        SET balance = :new_balance
        WHERE id = :id
        RETURNING balance
        """,
        id=current_user.id, 
        new_balance=new_balance)

        current_user.balance = new_balance
        return current_user.balance
        
    @staticmethod
    def sub_balance(amount):
        new_balance = current_user.balance
        
        if amount != None and amount <= current_user.balance:
            new_balance = new_balance - amount
            

        
        rows = app.db.execute("""
        UPDATE Users
        SET balance = :new_balance
        WHERE id = :id
        RETURNING balance
        """,
        id=current_user.id, 
        new_balance=new_balance)

        current_user.balance = new_balance
        return current_user.balance
    
    '''
    UPDATE PROFILE METHODS
    '''
    
    @staticmethod
    def update_profile(name, email):
        new_name = current_user.name
        new_email = current_user.email
       
        if name != "":
            new_name = name
            
        if email != "":
            new_email = email
         

        rows = app.db.execute("""
        UPDATE Users
        SET name = :new_name, email = :new_email
        WHERE id = :id
        RETURNING name
        """,
        id=current_user.id, 
        new_name=new_name,
        new_email=new_email)

        current_user.name = new_name
        current_user.email = new_email
        return current_user.name   
    
    @staticmethod
    def update_profile_pic(image):

        rows = app.db.execute("""
        UPDATE Users
        SET image = :image
        WHERE id = :id
        RETURNING name
        """,
        id=current_user.id, 
        image=image)

        current_user.image = image;
        return current_user.image  
    
    '''
    REGISTRATION METHODS
    '''
    
    @staticmethod
    def email_exists(email):
        rows = app.db.execute("""
        SELECT email
        FROM Users
        WHERE email = :email
        """,
        email=email)
        return len(rows) > 0

    @staticmethod
    def register(email, password, name, balance, image):
        try:
            rows = app.db.execute("""
            INSERT INTO Users(email, password, name, balance, image)
            VALUES(:email, :password, :name, :balance, :image)
            RETURNING id, email, password, name, balance, image
            """,
        email=email,
        password=generate_password_hash(password),
        name=name,
        balance=balance,
        image=image)
            id = rows[0][0]
            return User.get(id)
        
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            return None


    @staticmethod
    def get_selected_user(id):
        rows = app.db.execute("""
        SELECT id, email, name, balance, image
        FROM Users
        WHERE id = :id
        """,
        id=id)
        return User(*(rows[0])) if rows else None
    
    @staticmethod
    def is_seller(id):
        rows = app.db.execute("""
        SELECT id
        FROM Sellers
        WHERE Sellers.id = :id
        """,
        id=id)
        if rows:
            return True
        return False

        
    @staticmethod
    @login.user_loader
    def get(id):
        rows = app.db.execute("""
        SELECT id, email, name, balance, image
        FROM Users
        WHERE id = :id
        """,
        id=id)
      
        return User(*(rows[0])) if rows else None


    