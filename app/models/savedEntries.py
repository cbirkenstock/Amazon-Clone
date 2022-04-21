from flask import current_app as app
from sqlalchemy import text
from sqlalchemy.sql.functions import user


class sflEntry:
	def __init__(self, user_id, product_id, name, price):
		self.user_id = user_id
		self.product_id = product_id
		self.name = name
		self.price = price

	@staticmethod
	def get_user_SFL(user_id):
		rows = app.db.execute('''
SELECT SavedForLater.user_id, SavedForLater.product_id, Products.name, CAST(Products.price as DECIMAL(12,2))
FROM SavedForLater, Products
WHERE SavedForLater.user_id = :user_id AND Products.product_id = SavedForLater.product_id
''', user_id = user_id)
		
		return [sflEntry(*row) for row in rows]

	@staticmethod
	def addItemBack(user_id, product_id):
		try:
			with app.db.engine.connect() as conn:
				conn.execute(text('INSERT INTO CartEntries VALUES (:user_id, :product_id, 1)'), user_id = user_id, product_id = product_id)
				conn.execute(text('DELETE FROM SavedForLater WHERE user_id = :user_id AND product_id = :product_id'), user_id = user_id, product_id = product_id)
				rows = conn.execute(text('SELECT  CartEntries.user_id, CartEntries.product_id, Products.name, CartEntries.quantity, CAST(CartEntries.quantity*Products.price as DECIMAL(12,2)) FROM CartEntries, Products WHERE CartEntries.user_id = :user_id AND CartEntries.product_id = Products.product_id AND CartEntries.product_id = :product_id'), user_id = user_id, product_id = product_id)
				return rows
		except Exception as ex:
			template = "An exception of type {0} occurred. Arguments: \n{1!r}"
			message = template.format(type(ex).__name__, ex.args)
			print(message)
			return None


	