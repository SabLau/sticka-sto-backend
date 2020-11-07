# This is a test to send test email to temp emails
# Implement functionalities into server.py


from flask import Flask
from flask_mail import Mail, Message
import os
app = Flask(__name__)

app.config['DEBUG'] = True
app.config['TESTING'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEBUG'] = True
app.config['MAIL_USERNAME'] = os.getenv('STICKA_STO_EMAIL')
app.config['MAIL_PASSWORD'] = os.getenv('STICKA_STO_EMAIL_PW')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('STICKA_STO_EMAIL')
app.config['MAIL_MAX_EMAILS'] = None
app.config['MAIL_SUPPRESS_SEND'] = False
app.config['MAIL_ASII_ATTACHMENTS'] = False

mail = Mail(app)

@app.route("/send_email")
def send_email():

    # Subject line of email
    msg = Message("Wassup 8008135",
                recipients = ["name@example.com"])
    # Email body
    msg.body = 'This is the body of the email'
    mail.send(msg)

    return 'Message has been sent!'


if __name__ == '__main__':
    app.run()


# Sending bulk emails 
# @app.route('/bulk')
# def bulk():
#     users = [{'name' : 'John', 'email' : 'johndoe@email.com'}]

#     with mail.connect() as conn:
#         for user in users:
#             msg = Message('Bulk!', recipients=[user.email])
#             msg.body = 'Your verfication code is' 
#             conn.send(msg)



# Sending the email with an attachment
# with app.open_resource("image.png") as fp:
#     msg.attach("image.png", "image/png", fp.read())


# Message types in Mail
# msg = Message(
#     subject = '',
#     recipients = [],
#     body = '',
#     html = '',
#     sender = '',
#     cc = [],
#     bcc = [],
#     attachments = [],
#     reply_to = [],
#     date = 'date',
#     charset = '',
#     extra_headers = {'':''},
#     mail_options = [],
#     rcpt_options = []
# )