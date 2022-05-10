import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from libraryapi.schemas import BookSerializer
from libraryapi.models import Book


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
        with sqlite3.connect("data.db") as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM books WHERE name=?"
            result = cursor.execute(query, (name,))
            row = result.fetchone()
        if row:
            try:
                book = Book(*row)
            except Exception:
                return {"message": "something went wrong"}, 500
            return BookSerializer(book).data, 200
        return {"message": f"no book with name {name}"}, 404

    @jwt_required()
    def post(self):
        args = self.parser.parse_args(strict=True)
        if next(filter(lambda b: b.name == args["name"], books), None) is not None:
            return {'message': "the book with name '{}' already exists.".format(args["name"])}, 400
        new_book = Book(args["name"], args["author"], args["pages"], args["price"])
        books.append(new_book)
        return BookSerializer(new_book).data, 201

    @jwt_required()
    def delete(self, name):
        # todo: implement check if book was actually deleted now it shows every time
        global books
        books = list(filter(lambda b: b.name != name, books))
        return {"message": "book deleted"}, 200

    @jwt_required()
    def put(self):
        args = self.parser.parse_args(strict=True)
        book = next(filter(lambda b: b.name == args["name"], books), None)
        if book is None:
            book = Book(args["name"], args["author"], args["pages"], args["price"])
            books.append(book)
        else:
            book.update(**args)
        return BookSerializer(book).data, 200


class BooksListApi(Resource):
    """api resource for /books endpoint, lists all books"""
    def get(self):
        return {"books": BookSerializer(books, many=True).data}, 200
