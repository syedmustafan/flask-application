import os

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_httpauth import HTTPBasicAuth


app = Flask(__name__)
auth = HTTPBasicAuth()

DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=os.environ.get("POSTGRES_USER"), \
    pw=os.environ.get("POSTGRES_PW"),url=os.environ.get("POSTGRES_URL"),db=os.environ.get("POSTGRES_DB"))

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=False, nullable=True)
    password = db.Column(db.String(200), unique=False, nullable=True)
    first_name = db.Column(db.String(200), unique=False, nullable=True)
    last_name = db.Column(db.String(200), unique=False, nullable=True)

    def __repr__(self): 
        return '<id {}>'.format(self.username)


@app.route('/login', methods = ['POST'])
def get_resource():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        return jsonify({"message":"Missing password or username"}), 400
    elif User.query.filter_by(username = username, password=password).first():
        return jsonify({"message":"You are successfully logged in!"}), 200
    else:
        return jsonify({"message":"Wrong Username or Password!"}), 401  


@app.route('/create/users', methods = ['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    first_name = request.json.get('first_name')
    last_name = request.json.get('last_name')
    if username is None or password is None:
        return jsonify({"message":"Missing password or username"}), 400
    elif User.query.filter_by(username = username).first() is not None:
        return jsonify({"message":"Existing User"}), 400
    user = User(username = username, password=password,first_name=first_name, last_name=last_name)
    db.session.add(user)
    db.session.commit()
    return jsonify({ "message": "User Successfully Created", 'data': {"User":user.username} }), 201

