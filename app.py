from flask import Flask
from flask_restful import Resource, Api, reqparse
from schemas.book import BookSerializer
from models.book import Book

app = Flask(__name__)
api = Api(app)

books = []


class BookApi(Resource):
    """
    Api resource bind to /book, /book/<params> endpoint
    """
    parser = reqparse.RequestParser()
    parser.add_argument("name", required=True, type=str)
    parser.add_argument("author", required=True, type=str)
    parser.add_argument("pages", required=True, type=int)
    parser.add_argument("price", required=True, type=float)

    def get(self, name: str):
        book = next(filter(lambda b: b.name == name, books), None)
        if book:
            return BookSerializer(book).data, 200
        return {"message": f"no book with name {name}"}, 404

    def post(self):
        args = self.parser.parse_args(strict=True)
        if next(filter(lambda b: b.name == args["name"], books), None) is not None:
            return {'message': "the book with name '{}' already exists.".format(args["name"])}, 400
        new_book = Book(args["name"], args["author"], args["pages"], args["price"])
        books.append(new_book)
        return BookSerializer(new_book).data, 201


class BooksListApi(Resource):
    """api resource for /books endpoint, lists all books"""
    def get(self):
        return {"books": BookSerializer(books, many=True).data}, 200


api.add_resource(BookApi, "/book/<string:name>", "/book")
api.add_resource(BooksListApi, "/books")

if __name__ == '__main__':
    app.run(debug=True)
