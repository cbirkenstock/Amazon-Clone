from flask import current_app as app


'''
CREATE TABLE Products (
    product_id INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    seller_id INT NOT NULL REFERENCES Sellers(id),
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

class OrderedItem:
    def __init__(self, order_id, product_id, name, fulfillment_status, quantity, price_paid, order_date, seller_id):
        self.order_id = order_id
        self.product_id = product_id
        self.name = name
        self.fulfillment_status = fulfillment_status
        self.quantity = quantity
        self.price_paid = price_paid
        self.order_date = order_date
        self.seller_id = seller_id

    @staticmethod
    def get_all_for_seller(available, fullfilment_status, seller_id):
        rows = app.db.execute('''
        SELECT orderedItems.order_id, orderedItems.product_id, products.name, orderedItems.fulfillment_status, orderedItems.quantity, orderedItems.price_paid, purchases.order_date, products.seller_id
        FROM orderedItems 
        JOIN products ON orderedItems.product_id = products.product_id
        Join purchases ON orderedItems.order_id = purchases.order_id
        WHERE available = :available
        AND orderedItems.fulfillment_status = :fullfilment_status
        AND products.seller_id = :seller_id
        ORDER BY purchases.order_date
        ''',
        available=available,
        fullfilment_status=fullfilment_status,
        seller_id=seller_id)

        return [OrderedItem(*row) for row in rows]

    @staticmethod
    def get_all(available, fullfilment_status):
        rows = app.db.execute('''
        SELECT orderedItems.order_id, orderedItems.product_id, products.name, orderedItems.fulfillment_status, orderedItems.quantity, orderedItems.price_paid, purchases.order_date, products.seller_id
        FROM orderedItems 
        JOIN products ON orderedItems.product_id = products.product_id
        Join purchases ON orderedItems.order_id = purchases.order_id
        WHERE available = :available
        AND orderedItems.fulfillment_status = :fullfilment_status
        ORDER BY purchases.order_date
        ''',
        available=available,
        fullfilment_status=fullfilment_status)

        return [OrderedItem(*row) for row in rows]

    @staticmethod
    def setItemFulfilled(product_id):
        rows = app.db.execute(
        '''
        UPDATE PRODUCTS
        SET fulfilled = True
        WHERE product_id = :product_id
        RETURNING product_id
        ''',
        product_id=product_id)
        return rows

    @staticmethod
    def get_most_popular_items(seller_id):
        topFive = []
        true = True

        topFive = app.db.execute(
        '''
        SELECT products.product_id, products.name, COUNT(orderedItems.product_id)
        FROM orderedItems 
        JOIN products ON orderedItems.product_id = products.product_id
        JOIN purchases ON orderedItems.order_id = purchases.order_id
        WHERE available = True
        AND products.seller_id = :seller_id
        GROUP BY products.product_id
        ORDER BY COUNT(orderedItems.product_id) DESC, products.name
        LIMIT 5
        ''',
        seller_id=seller_id)
        
        if len(topFive) < 5:
            topFive = app.db.execute(
            '''
            SELECT products.product_id, products.name, COUNT(orderedItems.product_id)
            FROM orderedItems 
            JOIN products ON orderedItems.product_id = products.product_id
            JOIN purchases ON orderedItems.order_id = purchases.order_id
            WHERE available = True
            GROUP BY products.product_id
            ORDER BY COUNT(orderedItems.product_id) DESC, products.name
            LIMIT 5
            '''
            )
            true = False

        ids = [];
        names = [];
        count = [];

        for item in topFive: 
            ids.append(item[0])
            names.append(item[1])
            count.append(item[2])

        rows = app.db.execute(
        '''
        SELECT products.name, COUNT(orderedItems.product_id), EXTRACT(MONTH FROM purchases.order_date)
        FROM orderedItems 
        JOIN products ON orderedItems.product_id = products.product_id
        Join purchases ON orderedItems.order_id = purchases.order_id
        WHERE available = True
        AND products.product_id = :id1 OR products.product_id = :id2 OR products.product_id = :id3 OR products.product_id = :id4 OR products.product_id = :id5
        GROUP BY EXTRACT(MONTH FROM purchases.order_date), products.name
        ''', 
        id1=ids[0],
        id2=ids[1], 
        id3=ids[2],
        id4=ids[3], 
        id5=ids[4]
        )

        return [names, rows, count, true]

    @staticmethod
    def get_purchase_history(user_id):
        purchaseIDs = app.db.execute(
        '''
        SELECT order_id
        FROM purchases
        '''
        )

        info = []

        for id in purchaseIDs:

            rows = app.db.execute(
            '''
            SELECT orderedItems.order_id, orderedItems.price_paid, products.name, purchases.num_items, purchases.total_amount, purchases.fulfillment_status 
            FROM orderedItems
            JOIN purchases ON orderedItems.order_id = purchases.order_id
            JOIN products ON orderedItems.product_id = orderedItems.product_id 
            '''
            )

            info.append([id, rows])

        return info 
    def getAllForOrder(order_id):
        try:
            rows = app.db.execute('''SELECT OrderedItems.order_id, OrderedItems.product_id, Products.name, OrderedItems.fulfillment_status, OrderedItems.quantity, OrderedItems.price_paid FROM OrderedItems, Products WHERE order_id = :order_id AND OrderedItems.product_id = Products.product_id''', order_id = order_id)
            return rows
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments: \n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            return None


    @staticmethod
    def get_all_by_order_id(order_id):
        rows = app.db.execute(
        '''
        SELECT * 
        FROM orderedItems
        WHERE order_id = :order_id
        ''',
        order_id=order_id)
        return rows

    @staticmethod
    def get_name(page_size, page_number, name, seller_id):
        rows = app.db.execute('''
        SELECT orderedItems.order_id, orderedItems.product_id, products.name, orderedItems.fulfillment_status, orderedItems.quantity, orderedItems.price_paid, purchases.order_date, products.seller_id
        FROM orderedItems 
        JOIN products ON orderedItems.product_id = products.product_id
        Join purchases ON orderedItems.order_id = purchases.order_id
        WHERE available = True
        AND products.seller_id = :seller_id
        AND products.name LIKE CONCAT('%', CAST(:name AS varchar), '%')
        ORDER BY purchases.order_date
        LIMIT :page_size OFFSET :page_number*:page_size
        ''',
                                  page_size=page_size,
                                  page_number=page_number,
                                  name=name,
                                  seller_id=seller_id)
        return [OrderedItem(*row) for row in rows]
    
    @staticmethod
    def fulfillOrder(order_id, product_id):
        rows = app.db.execute('''
        UPDATE OrderedItems
        SET fulfillment_status = True
        WHERE order_id = :order_id
        AND product_id = :product_id
        Returning order_id
        ''', 
        order_id=order_id,
        product_id=product_id)
        return rows

