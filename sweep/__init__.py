"""
File: __init__.py
Purpose: initializes the application
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object('config.BaseConfiguration')

db = SQLAlchemy(app)

from views.common import common
app.register_blueprint(common)

from sweep import models
