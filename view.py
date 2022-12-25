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


@app.route('/inbox/', methods=['GET', 'POST'])
@app.route('/inbox/<int:mail_id>', methods=['GET', 'POST'])
def inbox(mail_id):
    if 'updateBD' in request.form:
        controller.update_emails()
    elif 'sendNew' in request.form:
        return redirect('/send')
    mails = controller.get_all_emails()
    cur_mail = controller.get_email(mail_id)
    print(cur_mail)
    return render_template(
        'inbox.html',
        email_address=app.config['MAIL_USERNAME'],
        mails=mails,
        cur_mail=controller.get_email(mail_id)
    )


@app.route('/sent', methods=['GET', 'POST'])
def sent():
    if 'updateBD' in request.form:
        controller.update_emails()
    elif 'sendNew' in request.form:
        return redirect('/send')
    return render_template('sent.html', email_address=app.config['MAIL_USERNAME'])


@app.route('/spam', methods=['GET', 'POST'])
def spam():
    if 'updateBD' in request.form:
        controller.update_emails()
    elif 'sendNew' in request.form:
        return redirect('/send')
    return render_template('spam.html', email_address=app.config['MAIL_USERNAME'])


@app.route('/trash', methods=['GET', 'POST'])
def trash():
    if 'updateBD' in request.form:
        controller.update_emails()
    elif 'sendNew' in request.form:
        return redirect('/send')
    return render_template('trash.html', email_address=app.config['MAIL_USERNAME'])


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
                          request.form['letterText'], False)
        return redirect('inbox/1')

    return render_template('send.html', sender=app.config['MAIL_USERNAME'])
