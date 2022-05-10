from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from libraryapi.security import authenticate, identity
from libraryapi.resources.user_register import UserRegister
from libraryapi.resources.book import BookApi, BooksListApi


# class AuthorListApi(Resource):
#     def get(self):
#         return {"authors": None}


def create_app():
    """
    Factory for creating flask app
    :return app
    """

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object("config.settings")
    app.config.from_pyfile("settings.py", silent=True)

    jwt = JWT(app, authenticate, identity)
    # Api extension register and resources initialization
    api = Api(app)
    api.add_resource(BookApi, "/book/<string:name>", "/book")
    api.add_resource(BooksListApi, "/books")
    # api.add_resource(AuthorListApi, "/authors")
    api.add_resource(UserRegister, "/register")
    return app
