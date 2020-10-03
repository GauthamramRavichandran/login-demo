import redis

redis_db = redis.Redis( host = "localhost",
                        port = 6379,
                        db   = 0)


class User:
	def __init__(self, name, email, password):
		self.name = name
		self.email = email
		self.password = password
		
	def save( self ):
		redis_db.set(self.email, self.password)
	
	@staticmethod
	def find_by_mail( email ) -> bytes:
		return redis_db.get(email)
