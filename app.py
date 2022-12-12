from flask import Flask
# from flask_mail import Message, Mail
from flask_sqlalchemy import SQLAlchemy
from config import AppConfiguration

# Create Flask application
app = Flask(__name__)
app.config.from_object(AppConfiguration)

db = SQLAlchemy(app)


# if __name__ == '__main__':
#     app.run(debug=True)
