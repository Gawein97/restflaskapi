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
        row = self.find_by_name(name)
        if row:
            try:
                book = Book(*row)
            except Exception:
                return {"message": "something went wrong"}, 500
            return BookSerializer(book).data, 200
        return {"message": f"no book with name {name}"}, 404

    @classmethod
    def find_by_name(cls, name):
        with sqlite3.connect("data.db") as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM books WHERE name=?"
            result = cursor.execute(query, (name,))
            row = result.fetchone()
        return row

    @classmethod
    def insert(cls, book):
        with sqlite3.connect("data.db") as conn:
            cursor = conn.cursor()
            query = "INSERT INTO books VALUES (?, ?, ?, ?)"
            cursor.execute(query, (book.name, book.author, book.pages, book.price))
            conn.commit()

    @classmethod
    def update(cls, book):
        with sqlite3.connect("data.db") as conn:
            cursor = conn.cursor()
            query = """
            UPDATE books
            SET name=?,
                author=?,
                pages=?,
                price=?
            WHERE name=?
            """
            cursor.execute(query, (book.name, book.author, book.pages, book.price, book.name))
            conn.commit()

    @jwt_required()
    def post(self):
        args = self.parser.parse_args(strict=True)
        if self.find_by_name(args["name"]):
            return {'message': "the book with name '{}' already exists.".format(args["name"])}, 400
        new_book = Book(args["name"], args["author"], args["pages"], args["price"])
        try:
            self.insert(new_book)
        except:
            return {"message": "error occurred"}, 500
        return BookSerializer(new_book).data, 201

    @jwt_required()
    def delete(self, name):
        # todo: implement check if book was actually deleted now it shows every time
        row = self.find_by_name(name)
        if not row:
            return {"message": "book doesn't exist"}, 400
        with sqlite3.connect("data.db") as conn:
            cursor = conn.cursor()
            query = "DELETE FROM books WHERE name=?"
            cursor.execute(query, (name,))
            conn.commit()
        return {"message": "book deleted"}, 200

    @jwt_required()
    def put(self):
        args = self.parser.parse_args(strict=True)
        row = self.find_by_name(args["name"])
        book = Book(args["name"], args["author"], args["pages"], args["price"])
        if row is None:
            try:
                self.insert(book)
            except:
                return {"message": "error occurred"}, 500
        else:
            try:
                self.update(book)
            except:
                return {"message": "error occurred"}, 500
        return BookSerializer(book).data, 200


class BooksListApi(Resource):
    """api resource for /books endpoint, lists all books"""
    def get(self):
        with sqlite3.connect("data.db") as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM books"
            result = cursor.execute(query)
            # This looks like a pile of garbage should change serializer to Marshall
            # TODO: Change serializer to Marshall or refactor code idk
            books = [Book(*b) for b in result.fetchall()]
        return {"books": BookSerializer(books, many=True).data}, 200
