from app import db


class Emails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    folder = db.Column(db.String(50))
    sender = db.Column(db.String(50))
    receiver = db.Column(db.String(50))
    subject = db.Column(db.Text())
    body = db.Column(db.Text())

    def __int__(self, folder, sender, receiver, subject, body):
        self.folder = folder
        self.sender = sender
        self.receiver = receiver
        self.subject = subject
        self.body = body
