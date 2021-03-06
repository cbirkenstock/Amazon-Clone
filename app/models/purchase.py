from flask import current_app as app
import datetime
from sqlalchemy import text

class Purchase:
    def __init__(self, order_id, user_id, total_amount, num_items, order_date, address, fulfillment_status):
        self.order_id = order_id
        self.user_id = user_id
        self.total_amount = total_amount
        self.num_items = num_items
        self.order_date = order_date
        self.address = address
        self.fulfillment_status = fulfillment_status


    '''
    given order id, get products

    CREATE TABLE OrderedItems (
 order_id INT NOT NULL REFERENCES Purchases(order_id),    
 product_id INT NOT NULL REFERENCES Products(product_id),  
 fulfillment_status BOOLEAN NOT NULL,
 quantity INT NOT NULL CHECK (quantity > 0),
 price_paid FLOAT NOT NULL CHECK (price_paid >= 0) 
);


CREATE TABLE Products (
    product_id INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    seller_id INT NOT NULL REFERENCES Users(id),
    name VARCHAR(255) NOT NULL,
    quantity INTEGER NOT NULL,
    category VARCHAR(256) NOT NULL,
    description VARCHAR(4096) NOT NULL, 
    price FLOAT NOT NULL,
    available BOOLEAN DEFAULT TRUE,
    image VARCHAR(256) NOT NULL,    
    CHECK (quantity >= 0),
    CHECK (price >= 0)
);
    '''
    @staticmethod
    def get_products(order_id):
        products = []
        rows = app.db.execute("""
        SELECT Products.name
        FROM OrderedItems, Products
        WHERE OrderedItems.order_id = :order_id
        AND OrderedItems.product_id = Products.product_id
        """,
            order_id=order_id)

        if(rows):
            for row in rows:
                products.append(row.name)
        
        return products

    @staticmethod
    def get_all_oids(user_id):
        rows = app.db.execute('''
        SELECT order_id
        FROM Purchases
        WHERE user_id = :user_id
        ''',
            user_id=user_id)

        return [Purchase(*row) for row in rows]

    @staticmethod
    def get_all_by_nothing():
        
        rows = app.db.execute('''
        SELECT *
        FROM Purchases
        ORDER BY order_date DESC
        ''',
            )

        return [Purchase(*row) for row in rows]

    @staticmethod
    def get_all_by_uid_since(user_id):
        rows = app.db.execute('''
        SELECT *
        FROM Purchases
        WHERE user_id = :user_id
        ORDER BY order_date DESC
        ''',
            user_id = user_id)

        return [Purchase(*row) for row in rows]

    @staticmethod
    def get_all_by_nothing_ASC():
        rows = app.db.execute('''
        SELECT *
        FROM Purchases
        ORDER BY order_date ASC
        ''',
            )

        return [Purchase(*row) for row in rows]

    @staticmethod
    def get_all_by_uid_since_ASC(user_id):
        rows = app.db.execute('''
        SELECT *
        FROM Purchases
        WHERE user_id = :user_id
        
        ORDER BY order_date ASC
        ''',
            user_id = user_id)

        return [Purchase(*row) for row in rows]

    @staticmethod
    def get_nothing_order_id(order_id):
        
        rows = app.db.execute('''
        SELECT *
        FROM Purchases
        WHERE CAST(order_id AS varchar) LIKE CONCAT('%', :order_id, '%')
        
        
        ORDER BY order_date DESC
        ''',
                              
                              order_id=order_id)
        return [Purchase(*row) for row in rows]
    
    @staticmethod
    def get_order_id(user_id, order_id):
        rows = app.db.execute('''
        SELECT *
        FROM Purchases
        WHERE CAST(order_id AS varchar) LIKE CONCAT('%', :order_id, '%')
        AND user_id = :user_id
        
        ORDER BY order_date DESC
        ''',
                              user_id = user_id,
                              order_id=order_id)
        return [Purchase(*row) for row in rows]

    @staticmethod
    def get_nothing_order_id_ASC(order_id):
        rows = app.db.execute('''
        SELECT *
        FROM Purchases
        WHERE CAST(order_id AS varchar) LIKE CONCAT('%', :order_id, '%')
        
        ORDER BY order_date ASC
        ''',
                              
                              order_id=order_id,)
        return [Purchase(*row) for row in rows]
    
    @staticmethod
    def get_order_id_ASC(user_id, order_id):
        rows = app.db.execute('''
        SELECT *
        FROM Purchases
        WHERE CAST(order_id AS varchar) LIKE CONCAT('%', :order_id, '%')
        AND user_id = :user_id
        ORDER BY order_date ASC
        ''',
                              user_id = user_id,
                              order_id=order_id)
        return [Purchase(*row) for row in rows]
    
    @staticmethod
    def getUserOrders(user_id):
        rows = app.db.execute('''SELECT order_id FROM Purchases WHERE user_id = :user_id''', user_id = user_id)
        return rows

    @staticmethod
    def getUserFromPurchase(order_id):
        rows = app.db.execute('''SELECT user_id FROM Purchases WHERE order_id = :order_id''', order_id = order_id)
        return rows[0][0]

    @staticmethod
    def getDateFromPurchase(order_id):
        rows = app.db.execute('''SELECT order_date FROM Purchases WHERE order_id = :order_id''', order_id = order_id)
        return rows[0][0]

    @staticmethod
    def getAddrFromPurchase(order_id):
        rows = app.db.execute('''SELECT address FROM Purchases WHERE order_id = :order_id''', order_id = order_id)
        return rows[0][0]

    @staticmethod
    def checkOrderFulfilled(order_id):
        rows = app.db.execute('''SELECT * FROM OrderedItems WHERE order_id = :order_id AND fulfillment_status IS FALSE''', order_id = order_id)
        if rows == None:
            app.db.execute('''UPDATE Purchases SET fulfillment_status = TRUE WHERE order_id = :order_id''')
            return True
        return False
    
    @staticmethod
    def getStatus(order_id):
        rows = app.db.execute('''SELECT fulfillment_status FROM Purchases WHERE order_id = :order_id''', order_id = order_id)
        return rows[0][0]
    
    @staticmethod
    def getPrice(order_id):
        rows = app.db.execute('''SELECT total_amount FROM Purchases WHERE order_id = :order_id ''', order_id = order_id)
        return rows[0][0]


    @staticmethod
    def logOrder(user_id, total_amount, num_items, address):
        try:
            with app.db.engine.connect() as conn:
                #moving unavailable items
                conn.execute(text('INSERT INTO SavedForLater(user_id, product_id) SELECT CartEntries.user_id, CartEntries.product_id FROM CartEntries, Products WHERE CartEntries.user_id = :user_id AND Products.product_id = CartEntries.product_id AND Products.quantity < CartEntries.quantity'), user_id = user_id)
                conn.execute(text('DELETE FROM CartEntries WHERE CartEntries.product_id IN (SELECT CartEntries.product_id FROM CartEntries, Products WHERE CartEntries.user_id = :user_id AND CartEntries.product_id = Products.product_id AND Products.quantity < CartEntries.quantity)'), user_id = user_id)
                conn.execute(text('INSERT INTO SavedForLater(user_id, product_id) SELECT CartEntries.user_id, CartEntries.product_id FROM CartEntries, Products WHERE CartEntries.user_id = :user_id AND Products.product_id = CartEntries.product_id AND Products.available IS FALSE'), user_id = user_id)
                conn.execute(text('DELETE FROM CartEntries WHERE CartEntries.product_id IN (SELECT CartEntries.product_id FROM CartEntries, Products WHERE CartEntries.user_id = :user_id AND CartEntries.product_id = Products.product_id AND Products.available IS FALSE)'), user_id = user_id)
                op = app.db.execute('''SELECT Products.price, CartEntries.quantity FROM Products, CartEntries WHERE CartEntries.user_id = :user_id AND CartEntries.product_id = Products.product_id''', user_id = user_id)
                               #checking price and bal
                orderPrice = 0
                for row in op:
                    orderPrice += (row[0] * row[1])
                userBal = app.db.execute('''SELECT Balance FROM Users WHERE id = :user_id''', user_id = user_id)
                userBal = userBal[0][0]
                if(orderPrice > userBal):
                    conn.rollback()
                    return False
                #updating tables
                purchaserows = app.db.execute('''INSERT INTO Purchases(user_id, total_amount, num_items, order_date, address, fulfillment_status)VALUES(:user_id, :total_amount, :num_items, :order_date, :address, FALSE) RETURNING order_id, user_id, total_amount, num_items, order_date, address, fulfillment_status''', user_id = user_id, total_amount = total_amount, num_items = num_items, order_date = datetime.datetime.now(), address = address)
                order_id = purchaserows[0][0]
                cartrows = app.db.execute('''SELECT * FROM CartEntries WHERE user_id = :user_id''', user_id = user_id)
                for n in cartrows:
                    price = app.db.execute('''SELECT Price FROM Products WHERE product_id = :product_id''', product_id = n[1])
                    quantity = app.db.execute('''SELECT quantity FROM CartEntries WHERE product_id = :product_id AND user_id = :user_id''', product_id = n[1], user_id = user_id)
                    realprice = (price[0][0] * quantity[0][0])
                    conn.execute(text('INSERT INTO OrderedItems VALUES(:order_id, :product_id, :bool, :quantity, :price)'), order_id = order_id, product_id = n[1], bool = False, quantity = n[2], price=realprice)
                    conn.execute(text('DELETE FROM CartEntries WHERE user_id = :user_id AND product_id = :product_id'), user_id = user_id, product_id = n[1])
                    conn.execute(text('UPDATE Products SET quantity = quantity - :quan WHERE product_id = :product_id'), quan = quantity[0][0], product_id = n[1])
                    conn.execute(text('UPDATE Users SET balance = balance - :realprice WHERE id = :user_id'), realprice = realprice, user_id = user_id)
                    sellerid = app.db.execute('''SELECT seller_id FROM Products WHERE product_id = :product_id''', product_id = n[1])
                    conn.execute(text('UPDATE Users SET balance = balance + :realprice WHERE id = :sellerid'), sellerid = sellerid[0][0], realprice = realprice)
            return order_id
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            return None

