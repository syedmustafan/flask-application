from flask import request, jsonify

from app import app
from .models import User
from app import db


@app.route('/login', methods=['POST'])
def get_resource():
    username = request.json.get('username')
    password = request.json.get('password')
    user = User.query.filter_by(username=username).first()
    if username is None or password is None:
        return jsonify({"message": "Missing password or username"}), 400
    elif user and user.verify_password(password):
        return jsonify({"message": "You are successfully logged in!"}), 200
    else:
        return jsonify({"message": "Wrong Username or Password!"}), 401


@app.route('/create/users', methods=['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    first_name = request.json.get('first_name')
    last_name = request.json.get('last_name')
    if username is None or password is None:
        return jsonify({"message": "Missing password or username"}), 400
    elif User.query.filter_by(username=username).first() is not None:
        return jsonify({"message": "Existing User"}), 400
    user = User(username=username, first_name=first_name, last_name=last_name)
    user.hashing_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User Successfully Created", 'data': {"User": user.username}}), 201
