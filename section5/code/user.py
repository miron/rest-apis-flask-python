import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity


class User(Resource):
    def __init__(self, _id=0, username=None, password=None):
        self.id = _id
        self.username = username
        self.password = password


    # @jwt_required()
    # def get(self): # view all users
    #     user = current_identity
    #     return {'id': user.id, 'username': user.username, 'password': user.password}

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "username", type=str, required=True, help="Username cannot be left blank!"
    )
    parser.add_argument(
        "password", type=str, required=True, help="Password cannot be left blank!"
    )

    def post(self):
        data = UserRegister.parser.parse_args()
        if User.find_by_username(data["username"]):
            return {"message": "A user  with that username already exists"}, 400

        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "INSERT INTO users VALUES (NULL, ?, ?)"

        cursor.execute(query, (data["username"], data["password"]))

        connection.commit()
        connection.close()

        return {"message": "User created successfully."}, 201
