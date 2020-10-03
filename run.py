from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from app import User

myapp = Flask(__name__)


@myapp.route("/login", methods = ["POST"])
def login():
	email = request.form.get("email")
	password = request.form.get("password")
	pwhash = User.find_by_mail(email)
	if pwhash and check_password_hash(pwhash = pwhash.decode("utf-8"),
	                                  password = password):
		return jsonify({'message': 'Password is correct'})
	# might return a token that verifies the user in the future
	return jsonify({'error': 'Email or password is incorrect'}), 401


@myapp.route("/register", methods = ["POST"])
def register():
	email = request.form.get("email")
	name = request.form.get("name")
	password = request.form.get("password")
	try:
		User(name, email, generate_password_hash(password)).save()
	except Exception as e:
		return jsonify({'error': str(e)}), 500
	return jsonify({'message': 'User registered successfully'}), 201
	
	
if __name__ == "__main__":
	myapp.run(port = 6000)
