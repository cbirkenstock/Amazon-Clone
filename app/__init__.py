from flask import Flask
from flask_login import LoginManager
from flask_babel import Babel
from .config import Config
from .db import DB


login = LoginManager()
login.login_view = 'users.login'
babel = Babel()


def create_app():
    app = Flask(__name__, static_url_path='/static')
    app.config.from_object(Config)

    app.db = DB(app)
    login.init_app(app)
    babel.init_app(app)

    from .index import bp as index_bp
    app.register_blueprint(index_bp)

    from .users import bp as user_bp
    app.register_blueprint(user_bp)

    from .sellerDashboard import bp as sellerDashboard_bp
    app.register_blueprint(sellerDashboard_bp)

    from .reviews import bp as review_bp
    app.register_blueprint(review_bp)

    from .cart import bp as cart_bp
    app.register_blueprint(cart_bp)

    from .checkout import bp as checkout_bp
    app.register_blueprint(checkout_bp)

    from .orderConfirm import bp as order_bp
    app.register_blueprint(order_bp)

    return app
