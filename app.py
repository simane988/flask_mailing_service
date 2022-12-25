from flask import Flask
# from flask_mail import Message, Mail
from flask_sqlalchemy import SQLAlchemy
from config import AppConfiguration
# from model import Emails

# Create Flask application
app = Flask(__name__)

# Configure Mail app
app.config.from_object(AppConfiguration)

db = SQLAlchemy(app)
