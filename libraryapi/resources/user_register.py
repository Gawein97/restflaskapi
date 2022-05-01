import sqlite3
from flask_restful import Resource, reqparse


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username", required=True, type=str)
    parser.add_argument("password", required=True, type=str)

    def post(self):
        args = self.parser.parse_args(strict=True)
        with sqlite3.connect("data.db") as conn:
            cursor = conn.cursor()
            query = "INSERT INTO users VALUES (NULL, ?, ?)"
            cursor.execute(query, (args["username"], args["password"]))

            conn.commit()
        return {"message": "user created"}, 201
