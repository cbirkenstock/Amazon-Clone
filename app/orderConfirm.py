from .models.purchase import Purchase
from .models.orderedItem import OrderedItem
from flask_login import current_user
from flask import render_template, redirect, url_for
from flask import Blueprint


bp = Blueprint('order', __name__)


@bp.route('/order/<int:order_id>', methods=['GET', 'POST'])
def order(order_id):
    if current_user.is_authenticated:
        Purchase.checkOrderFulfilled(order_id)
        if(Purchase.getUserFromPurchase(order_id) == current_user.id):
            items = OrderedItem.getAllForOrder(order_id)
            date = Purchase.getDateFromPurchase(order_id)
            address = Purchase.getAddrFromPurchase(order_id)
            status = Purchase.getStatus(order_id)
            finalprice = Purchase.getPrice(order_id)
            return render_template('orderPage.html', order_id = order_id, order_date = date, items = items, address = address, status = status, finalprice = finalprice)
        else:
            return(redirect(url_for('users.profile')))
        
    else:
        return(redirect(url_for('users.login')))

