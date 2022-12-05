from flask import Flask, render_template
from flask_mail import Message, Mail
import config as conf

# Create Flask application
app = Flask(__name__)

# Configure Mail app
app.config['MAIL_SERVER'] = conf.MAIL_SERVER
app.config['MAIL_PORT'] = conf.MAIL_PORT
app.config['MAIL_USERNAME'] = conf.MAIL_USERNAME
app.config['MAIL_PASSWORD'] = conf.MAIL_PASSWORD
app.config['MAIL_USE_TLS'] = conf.MAIL_USE_TLS
app.config['MAIL_USE_SSL'] = conf.MAIL_USE_SSL

# Create Mail app
mail = Mail(app)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
