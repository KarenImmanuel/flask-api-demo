#!flask/bin/python
import json

from flask import Flask, jsonify, abort, request

from email_api import send_email

app = Flask(__name__)

with open('books.json', 'r') as books_file:
    books = json.loads(books_file.read()) 

@app.route('/api/v1.0/books', methods=['POST'])
def create_book():
    if not request.json or not 'stars' in request.json:
        abort(400)
    book = {
        'id': books[-1]['id'] + 1,
        'stars': request.json['stars'],
        'price': request.json.get('price', ""),
        'done': False
    }
    books.append(book)
    return jsonify({'book': book}), 201


@app.route('/api/v1.0/books', methods=['GET'])
def get_books():
    return jsonify({'books': books})



@app.route('/api/v1.0/books<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = [book for book in books if book['id'] == book_id]
    if len(book) == 0:
        abort(404)
    return jsonify({'book': book[0]})

@app.route('/api/v1.0/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = [book for book in books if book['id'] == book_id]
    if len(book) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'stars' in request.json and type(request.json['stars']) != unicode:
        abort(400)
    if 'price' in request.json and type(request.json['price']) is not unicode:
        abort(400)
    book[0]['stars'] = request.json.get('stars', book[0]['stars'])
    book[0]['price'] = request.json.get('price', book[0]['price'])
    return jsonify({'book': book[0]})

@app.route('/api/v1.0/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = [book for book in books if book['id'] == book_id]
    if len(book) == 0:
        abort(404)
    books.remove(book[0])
    return jsonify({'result': True})


@app.route('/api/v1.0/email_books', methods=['GET'])
def email_books():
    send_email('List of books', 'aa@abc.com', ['bb@abc.com'], books, None)
    return jsonify({'books': books})

if __name__ == '__main__':
    app.run(debug=True)