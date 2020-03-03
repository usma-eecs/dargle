from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dargle.sqlite'
db = SQLAlchemy(app)

db.Model.metadata.reflect(db.engine)

from dargle_webapp import routes
