from email import encoders
from email.header import decode_header
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from tqdm import tqdm
from app import app
from app import db
from model import Emails

import base64
import email
import smtplib
import imaplib
import mimetypes
import time
import config
import os

folders_dict = {
    'INBOX': "INBOX",
    'SENT': '(\\HasNoChildren \\Unmarked \\Sent) "|" "&BB4EQgQ,BEAEMAQyBDsENQQ9BD0ESwQ1-"',
    'SPAM': "SPAM",
    'TRASH': "TRASH",
    'DRAFTS': "DRAFTS",
    'UNMARKED': "UNMARKED",
}


def send_email(sender, recipient, subject, body_text, is_html=False, attachments=''):
    server = smtplib.SMTP_SSL(app.config['MAIL_SEND_SERVER'], app.config['MAIL_SEND_PORT'])

    if app.config['MAIL_USE_TLS']:
        server.starttls()

    try:
        server.login(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])

        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = recipient
        msg['Subject'] = subject

        if is_html:
            msg.attach(MIMEText(body_text, 'html'))
        else:
            msg.attach(MIMEText(body_text))

        if attachments != '':
            for file in tqdm(os.listdir(attachments)):
                time.sleep(0.4)
                filename = os.path.basename(file)
                ftype, encoding = mimetypes.guess_type(file)
                file_type, subtype = ftype.split('/')

                if file_type == 'text':
                    with open(f'attachments/{file}') as f:
                        file = MIMEText(f.read())
                elif file_type == 'image':
                    with open(f'attachments/{file}', 'rb') as f:
                        file = MIMEImage(f.read(), subtype)
                elif file_type == 'audio':
                    with open(f'attachments/{file}', 'rb') as f:
                        file = MIMEAudio(f.read(), subtype)
                elif file_type == 'application':
                    with open(f'attachments/{file}', 'rb') as f:
                        file = MIMEApplication(f.read(), subtype)
                else:
                    with open(f'attachments/{file}', 'rb') as f:
                        file = MIMEBase(file_type, subtype)
                        file.set_payload(f.read())
                        encoders.encode_base64(file)

                # with open(f'attachments/{file}', 'rb') as f:
                #     file = MIMEBase(file_type, subtype)
                #     file.set_payload(f.read())
                #     encoders.encode_base64(file)

                file.add_header('content-disposition', 'attachment', filename=filename)
                msg.attach(file)

        server.sendmail(sender, sender, msg.as_string())

        return 'Send successfully'
    except Exception as _ex:
        print(_ex)
        return f'{_ex}\nCheck your login or password please!'


def clean(text):
    # clean text for creating a folder
    return ''.join(c if c.isalnum() else '_' for c in text)


def update_emails(mail_folder='INBOX', update_count=100):

    try:
        num_rows_deleted = db.session.query(Emails).delete()
        db.session.commit()
    except:
        db.session.rollback()

    server = imaplib.IMAP4_SSL(app.config['MAIL_RECEIVE_SERVER'], app.config['MAIL_RECEIVE_PORT'])

    try:
        server.login(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        status, messages = server.select(folders_dict[mail_folder])

        print(server.list())

        messages = int(messages[0])

        print(messages)

        for i in range(messages, messages - update_count, -1):
            res, msg = server.fetch(str(i), '(RFC822)')

            for response in msg:
                if isinstance(response, tuple):
                    # parse a bytes email into a message object
                    msg = email.message_from_bytes(response[1])
                    # decode the email subject
                    subject, encoding = decode_header(msg['Subject'])[0]
                    if isinstance(subject, bytes):
                        # if it's a bytes, decode to str
                        subject = subject.decode(encoding)
                    # decode email sender
                    from_address, encoding = decode_header(msg.get('From'))[0]
                    if isinstance(from_address, bytes):
                        from_address = from_address.decode(encoding)
                    print('Subject:', subject)
                    print('From:', from_address)
                    try:
                        for part in msg.walk():
                            if part.get_content_maintype() == 'text' and (part.get_content_subtype() in ('plain', 'html')):
                                body_text = base64.b64decode(part.get_payload()).decode()
                            else:
                                body_text =\
                                    f'At the moment I don\'t know how to display ' \
                                    f'{part.get_content_maintype()}/{part.get_content_subtype()} message'
                    except:
                        body_text = \
                            f'At the moment I don\'t know how to display {msg.get_content_type()} message'

                    print('Body Text:', body_text)
                    print('=' * 100)

                    db.session.add(Emails(folder=mail_folder, sender=from_address, receiver=app.config['MAIL_USERNAME'],
                                          subject=subject, body=body_text))

            db.session.commit()

    except Exception as _ex:
        print(_ex)


def get_all_emails(mail_folder='INBOX', get_count = 25):
    return Emails.query.filter_by(folder=mail_folder)


def get_email(email_id):
    return Emails.query.get(email_id)


def auth(login, password):
    try:
        server = imaplib.IMAP4_SSL(app.config['MAIL_RECEIVE_SERVER'], app.config['MAIL_RECEIVE_PORT'])
        print(f'{login}, {password}')
        server.login(login, password)
        print('LoggedIn!')
        server.abort()
    except:
        print('Invalid login or password!')
        return 1

    config.AppConfiguration.MAIL_USERNAME = login
    app.config['MAIL_USERNAME'] = login
    config.AppConfiguration.MAIL_PASSWORD = password
    app.config['MAIL_PASSWORD'] = password
    config.AppConfiguration.MAIL_AUTH = True
    app.config['MAIL_AUTH'] = True

    return 0
