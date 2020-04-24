from flask import Flask, request
from flask_mail import Mail, Message
from celery import Celery
import os

app = Flask(__name__)
mail = Mail(app)

app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'abhishek.g9321@gmail.com' # os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = 'Ab!5#5i@h' #os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = 'flask@example.com'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'], backend=app.config['CELERY_RESULT_BACKEND'])
celery.conf.update(app.config)


@celery.task
def send_mail(email_data):
    """Background task to send an email with Flask-Mail."""
    msg = Message(email_data['subject'],
                  sender=app.config['MAIL_DEFAULT_SENDER'],
                  recipients=[email_data['to']])
    msg.body = email_data['body']
    print(msg.body)
    with app.app_context():
        mail.send(msg)


@app.route('/', methods=['GET', 'POST'])
def index():
    email = request.args.get('email')
    print(email)
    # send the email
    #{'subject': 'Hello from Flask', 'to': 'agopalaiah@quotient.com', 'body': 'This is a test email sent from a background Celery task.'}
    email_data = {
        'subject': 'Hello from Flask',
        'to': 'agopalaiah@quotient.com',
        'body': 'This is a test email sent from a background Celery task.'
    }
    print(email_data)
    send_mail.delay(email_data)
    return 'sent mail'


if __name__ == '__main__':
    app.run()
