from flask import Flask
from flask_restful import Resource, Api, reqparse
from schemas.book import BookSerializer
from models.book import Book

app = Flask(__name__)
api = Api(app)

books = []


class BookApi(Resource):
    """
    Api resource binded to /book route
    """
    parser = reqparse.RequestParser()
    parser.add_argument("name", required=True, type=str)
    parser.add_argument("author", required=True, type=str)
    parser.add_argument("pages", required=True, type=int)
    parser.add_argument("price", required=True, type=float)

    def get(self, name: str):
        for b in books:
            if b.name == name:
                return BookSerializer(b).data
        return {"message": f"no book with name {name}"}

    def post(self):
        args = self.parser.parse_args()
        if next(filter(lambda b: b.name == args["name"], books), None) is not None:
            return {'message': "the book with name '{}' already exists.".format(args["name"])}, 400
        new_book = Book(args["name"], args["author"], args["pages"], args["price"])
        books.append(new_book)
        return BookSerializer(new_book).data


api.add_resource(BookApi, "/book/<string:name>", "/book/")

if __name__ == '__main__':
    app.run(debug=True)
