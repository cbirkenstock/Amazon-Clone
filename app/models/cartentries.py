from flask import current_app as app
from sqlalchemy import text
from sqlalchemy.sql.expression import false

'''
CREATE TABLE CartEntries (
	user_id INT NOT NULL REFERENCES Users(id),
	product_id INT NOT NULL REFERENCES PRODUCTS(product_id),
	quantity INT NOT NULL CHECK (quantity > 0),
	PRIMARY KEY(user_id, product_id)
);
'''

class CartEntry:
	def __init__(self, user_id, product_id, name, quantity, price):
		self.user_id = user_id
		self.product_id = product_id
		self.name = name
		self.quantity = quantity
		self.price = price

	@staticmethod
	def get_user_cart(user_id):
		rows = app.db.execute('''
SELECT  CartEntries.user_id, CartEntries.product_id, Products.name, CartEntries.quantity, CAST(CartEntries.quantity*Products.price as DECIMAL(12,2))
FROM CartEntries, Products
WHERE CartEntries.user_id = :user_id AND CartEntries.product_id = Products.product_id
''', user_id = user_id)
		
		return [CartEntry(*row) for row in rows]


	@staticmethod
	def save_whole_cart(user_id):
		try:
			with app.db.engine.connect() as conn:
				conn.execute(text('INSERT INTO SavedForLater(user_id, product_id) SELECT user_id, product_id FROM CartEntries WHERE user_id = :user_id'), user_id = user_id)
				conn.execute(text('DELETE FROM CartEntries WHERE user_id = :user_id'), user_id = user_id)
				rows = conn.execute(text('SELECT  CartEntries.user_id, CartEntries.product_id, Products.name, CartEntries.quantity, CAST(CartEntries.quantity*Products.price as DECIMAL(12,2)) FROM CartEntries, Products WHERE CartEntries.user_id = :user_id AND CartEntries.product_id = Products.product_id'), user_id = user_id)
			return [CartEntry(*row) for row in rows]
		except Exception as ex:
			template = "An exception of type {0} occurred. Arguments: \n{1!r}"
			message = template.format(type(ex).__name__, ex.args)
			print(message)
			return None


	@staticmethod
	def saveItem(user_id, product_id):
		try:
			with app.db.engine.connect() as conn:
				conn.execute(text('INSERT INTO SavedForLater VALUES (:user_id, :product_id)'), user_id = user_id, product_id = product_id)
				conn.execute(text('DELETE FROM CartEntries WHERE user_id = :user_id AND product_id = :product_id'), user_id = user_id, product_id = product_id)
				rows = conn.execute(text('SELECT * FROM SavedForLater WHERE user_id = :user_id AND product_id = :product_id'), user_id = user_id, product_id = product_id)
				return rows
		except Exception as ex:
			template = "An exception of type {0} occurred. Arguments: \n{1!r}"
			message = template.format(type(ex).__name__, ex.args)
			print(message)
			return None
	
	@staticmethod
	def delItem(user_id, product_id):
		try:
			with app.db.engine.connect() as conn:
				conn.execute(text('DELETE FROM CartEntries WHERE user_id = :user_id AND product_id = :product_id'), user_id = user_id, product_id = product_id)
			rows = []
			return rows
		except Exception as ex:
			template = "An exception of type {0} occurred. Arguments: \n{1!r}"
			message = template.format(type(ex).__name__, ex.args)
			print(message)
			return None
	
	@staticmethod
	def addItem(user_id, product_id):
		try:
			with app.db.engine.connect() as conn:
				conn.execute(text('INSERT INTO CartEntries VALUES (:user_id, :product_id, 1)'), user_id = user_id, product_id = product_id)
				return []
		except Exception as ex:
			template = "An exception of type {0} occurred. Arguments: \n{1!r}"
			message = template.format(type(ex).__name__, ex.args)
			print(message)
			return None
	
	@staticmethod
	def add1(user_id, product_id):
		try:
			with app.db.engine.connect() as conn:
				conn.execute(text('UPDATE CartEntries SET quantity = quantity + 1 WHERE user_id = :user_id AND product_id = :product_id'), user_id = user_id, product_id = product_id)
				return []
		except Exception as ex:
			template = "An exception of type {0} occurred. Arguments: \n{1!r}"
			message = template.format(type(ex).__name__, ex.args)
			print(message)
			return None
	
	@staticmethod
	def add5(user_id, product_id):
		try:
			with app.db.engine.connect() as conn:
				conn.execute(text('UPDATE CartEntries SET quantity = quantity + 5 WHERE user_id = :user_id AND product_id = :product_id'), user_id = user_id, product_id = product_id)
				return []
		except Exception as ex:
			template = "An exception of type {0} occurred. Arguments: \n{1!r}"
			message = template.format(type(ex).__name__, ex.args)
			print(message)
			return None

	@staticmethod
	def add10(user_id, product_id):
		try:
			with app.db.engine.connect() as conn:
				conn.execute(text('UPDATE CartEntries SET quantity = quantity + 10 WHERE user_id = :user_id AND product_id = :product_id'), user_id = user_id, product_id = product_id)
				return []
		except Exception as ex:
			template = "An exception of type {0} occurred. Arguments: \n{1!r}"
			message = template.format(type(ex).__name__, ex.args)
			print(message)
			return None
	
	@staticmethod
	def rem1(user_id, product_id):
		try:
			with app.db.engine.connect() as conn:
				conn.execute(text('UPDATE CartEntries SET quantity = quantity - 1 WHERE user_id = :user_id AND product_id = :product_id'), user_id = user_id, product_id = product_id)
				return []
		except Exception as ex:
			template = "An exception of type {0} occurred. Arguments: \n{1!r}"
			message = template.format(type(ex).__name__, ex.args)
			print(message)
			return None
	
	@staticmethod
	def rem5(user_id, product_id):
		try:
			with app.db.engine.connect() as conn:
				conn.execute(text('UPDATE CartEntries SET quantity = quantity - 5 WHERE user_id = :user_id AND product_id = :product_id'), user_id = user_id, product_id = product_id)
				return []
		except Exception as ex:
			template = "An exception of type {0} occurred. Arguments: \n{1!r}"
			message = template.format(type(ex).__name__, ex.args)
			print(message)
			return None
	
	@staticmethod
	def rem10(user_id, product_id):
		try:
			with app.db.engine.connect() as conn:
				conn.execute(text('UPDATE CartEntries SET quantity = quantity - 10 WHERE user_id = :user_id AND product_id = :product_id'), user_id = user_id, product_id = product_id)
				return []
		except Exception as ex:
			template = "An exception of type {0} occurred. Arguments: \n{1!r}"
			message = template.format(type(ex).__name__, ex.args)
			print(message)
			return None
	
	@staticmethod
	def getFullPrice(user_id):
		try:
			with app.db.engine.connect() as conn:
				price = conn.execute(text('SELECT Products.price, CartEntries.quantity FROM Products, CartEntries WHERE CartEntries.user_id = :user_id AND CartEntries.product_id = Products.product_id'), user_id = user_id)
				count = 0
				for row in price:
					count += (row['price'] * row['quantity'])
				return round(count, 2)
			
		except Exception as ex:
			template = "An exception of type {0} occurred. Arguments: \n{1!r}"
			message = template.format(type(ex).__name__, ex.args)
			print(message)
			return None


	@staticmethod
	def checkInventory(user_id):
		try:
			with app.db.engine.connect() as conn:
				conn.execute(text('INSERT INTO SavedForLater(user_id, product_id) SELECT CartEntries.user_id, CartEntries.product_id FROM CartEntries, Products WHERE CartEntries.user_id = :user_id AND Products.product_id = CartEntries.product_id AND Products.quantity < CartEntries.quantity'), user_id = user_id)
				conn.execute(text('DELETE FROM CartEntries WHERE CartEntries.product_id IN (SELECT CartEntries.product_id FROM CartEntries, Products WHERE CartEntries.user_id = :user_id AND CartEntries.product_id = Products.product_id AND Products.quantity < CartEntries.quantity)'), user_id = user_id)
				conn.execute(text('INSERT INTO SavedForLater(user_id, product_id) SELECT CartEntries.user_id, CartEntries.product_id FROM CartEntries, Products WHERE CartEntries.user_id = :user_id AND Products.product_id = CartEntries.product_id AND Products.available IS FALSE'), user_id = user_id)
				conn.execute(text('DELETE FROM CartEntries WHERE CartEntries.product_id IN (SELECT CartEntries.product_id FROM CartEntries, Products WHERE CartEntries.user_id = :user_id AND CartEntries.product_id = Products.product_id AND Products.available IS FALSE)'), user_id = user_id)
			return []
		except Exception as ex:
			template = "An exception of type {0} occurred. Arguments: \n{1!r}"
			message = template.format(type(ex).__name__, ex.args)
			print(message)
			return None


	@staticmethod
	def getNumItems(user_id):
		try:
				with app.db.engine.connect() as conn:
						num = conn.execute(text('SELECT quantity FROM CartEntries WHERE user_id = :user_id'), user_id = user_id)
						count = 0
						for row in num:
								count += row['quantity']
						return count
		except Exception as ex:
				template = "An exception of type {0} occurred. Arguments: \n{1!r}"
				message = template.format(type(ex).__name__, ex.args)
				print(message)
				return None


				
				