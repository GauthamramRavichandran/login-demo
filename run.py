from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from app import User
import string
import random

import redis
redis_db = redis.Redis( host = "localhost",
                        port = 6379,
                        db   = 0)


def get_a_token(length = 15):
	choice = string.ascii_letters + string.digits
	token = ''.join(random.choice(choice) for _ in range(length))
	return token


myapp = Flask(__name__)


@myapp.route("/login", methods = ["POST"])
def login():
	email = request.form.get("email")
	password = request.form.get("password")
	user = User.find_by_mail(email)
	pwhash = user['password']
	if user and check_password_hash(pwhash = pwhash,
	                                password = password):
		token = get_a_token()
		redis_db.set(token, email)
		return jsonify({'message': 'Password is correct',
		                'token': token})
	# might return a token that verifies the user in the future
	return jsonify({'error': 'Email or password is incorrect'}), 401


@myapp.route("/register", methods = ["POST"])
def register():
	email = request.form.get("email")
	name = request.form.get("name")
	password = request.form.get("password")
	try:
		User(name, email, generate_password_hash(password)).save()
		token = get_a_token()
		redis_db.set(token, email)
	except Exception as e:
		return jsonify({'error': str(e)}), 500
	return jsonify({'message': 'User registered successfully',
	                'token': token}), 201
	
	
if __name__ == "__main__":
	myapp.run(port = 80)
