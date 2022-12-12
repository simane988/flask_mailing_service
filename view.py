from app import app
from flask import render_template, request, redirect

import config as conf
import controller


@app.route('/')
def index():
    if app.config['MAIL_AUTH']:
        return redirect('inbox')
    else:
        return redirect('auth')


@app.route('/inbox')
def inbox():
    controller.get_email_headers()
    return render_template('inbox.html', email_adress=app.config['MAIL_USERNAME'])


@app.route('/sent')
def sent():
    controller.get_email_headers('SENT')
    return render_template('sent.html', email_adress=app.config['MAIL_USERNAME'])


@app.route('/spam')
def spam():
    controller.get_email_headers('SPAM')
    return render_template('spam.html', email_adress=app.config['MAIL_USERNAME'])


@app.route('/trash')
def trash():
    controller.get_email_headers('TRASH')
    return render_template('trash.html', email_adress=app.config['MAIL_USERNAME'])


@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if "submitAuth" in request.form:
        print('Lets login!')
        if controller.auth(request.form['email'], request.form['password']) == 0:
            return redirect('/')

    return render_template('auth.html')


@app.route('/logout')
def logout():
    pass


@app.route('/send', methods=['GET', 'POST'])
def send():
    if "submitSend" in request.form:
        controller.send_email(app.config['MAIL_USERNAME'], request.form['sendTo'], request.form['letterSubject'],
                          request.form['letterText'], False, request.form['letterAttach'])
        return redirect('inbox')

    return render_template('send.html', sender=app.config['MAIL_USERNAME'])
