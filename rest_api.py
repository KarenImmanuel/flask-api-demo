#!flask/bin/python

"""implemented using the Flask-RESTful extension."""

from flask import Flask, jsonify, abort, make_response
from flask_restful import Api, Resource, reqparse, fields, marshal
from flask_httpauth import HTTPBasicAuth
from flask_user import login_required, current_user


app = Flask(__name__, static_url_path="")
api = Api(app)
auth = HTTPBasicAuth()

with open('books.json', 'r') as books_file:
    books = json.loads(books_file.read()) 

from flask_restful import Api, Resource
'''
class BookListAPI(Resource):
    def get(self):
        pass

    def post(self):
        pass

class BookAPI(Resource):
    def get(self, id):
        pass

    def put(self, id):
        pass

    def delete(self, id):
        pass

api.add_resource(BookListAPI, '/api/v1.0/books', endpoint = 'books')
api.add_resource(BookAPI, '/api/v1.0/books/<int:id>', endpoint = 'book')
'''

book_fields = {
    'title': fields.String,
    'stars': fields.String,
    'price': fields.String,
    'link': fields.Url('book'),
    'picture': fields.Url('book')
}

class BookListAPI(Resource):
    # decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, required=True,
                                   help='No book title provided',
                                   location='json')
        self.reqparse.add_argument('stars', type=str, default="",
                                   location='json')
        super(BookListAPI, self).__init__()

    def get(self):
        return {'books': [marshal(book, book_fields) for book in books]}

    def post(self):
        args = self.reqparse.parse_args()
        book = {
            'id': books[-1]['id'] + 1 if len(books) > 0 else 1,
            'title': args['title'],
            'stars': args['stars'],
            'price': args['price']
        }
        books.append(book)
        return {'book': marshal(book, book_fields)}, 201


class BookAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, location='json')
        self.reqparse.add_argument('stars', type=str, location='json')
        self.reqparse.add_argument('price', type=str, location='json')
        super(BookAPI, self).__init__()

    def get(self, id):
        book = [book for book in books if book['id'] == id]
        if len(book) == 0:
            abort(404)
        return {'book': marshal(book[0], book_fields)}

    def put(self, id):
        book = [book for book in books if book['id'] == id]
        if len(book) == 0:
            abort(404)
        book = book[0]
        args = self.reqparse.parse_args()
        for k, v in args.items():
            if v is not None:
                book[k] = v
        return {'book': marshal(book, book_fields)}

    def delete(self, id):
        book = [book for book in books if book['id'] == id]
        if len(book) == 0:
            abort(404)
        books.remove(book[0])
        return {'result': True}


api.add_resource(BookListAPI, '/todo/api/v1.0/books', endpoint='books')
api.add_resource(BookAPI, '/todo/api/v1.0/books/<int:id>', endpoint='book')


if __name__ == '__main__':
    app.run(debug=True)