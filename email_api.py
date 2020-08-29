import json
from flask_mail import Message
from flask import Flask, jsonify, abort, request

app = Flask(__name__)

from app import mail

from threading import Thread


with open('books.json', 'r') as books_file:
    books = json.loads(books_file.read()) 

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()


@app.route('/api/v1.0/email_books', methods=['GET'])
def email_books():
    send_email('List of books', 'aa@abc.com', ['bb@abc.com'], books, None)
    return jsonify({'books': books})

if __name__ == '__main__':
    app.run(debug=True)