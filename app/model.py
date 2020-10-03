from pymongo import MongoClient

client = MongoClient()
db = client["login-demo"].users


class User:
	def __init__(self, name, email, password):
		self.name = name
		self.email = email
		self.password = password
		
	def save( self ):
		db.insert_one({'name': self.name,
		               'email': self.email,
		               'password': self.password})
	
	@staticmethod
	def find_by_mail( email ):
		return db.find_one({'email': email})
