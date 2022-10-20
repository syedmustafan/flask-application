import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=os.environ.get("POSTGRES_USER"),
                                                               pw=os.environ.get("POSTGRES_PW"),
                                                               url=os.environ.get("POSTGRES_URL"),
                                                               db=os.environ.get("POSTGRES_DB"))

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import views
from app import models
