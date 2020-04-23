import datetime
from flask import Flask, jsonify, request, abort, make_response
from . import auth
from .. import db, http_auth
from app.models import User, Transaction, TransactionMonth

# log in an existing user
@auth.route("/login", methods=["POST"])
def login():
    """
    Required in body:

    email: String
    password: String
    """
    data = request.get_json(force=True)
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if (
        user is not None
        and user.password_hash is not None
        and user.verify_password(password)
    ):
        token = user.generate_auth_token()
        return jsonify({"user": user.serialize, "token": token.decode("ascii")})
    return "Wrong email or password!", 400


# check if token is valid and return user
@auth.route("/token", methods=["POST"])
def verify_token():
    """
    Required in body:

    token: String
    """
    data = request.get_json(force=True)
    token = data.get("token")

    user = User.verify_auth_token(token)
    if user is None:
        abort(404, "Token does not match any user")

    return jsonify(user.serialize)


# register a new user
@auth.route("/register", methods=["POST"])
def register():
    """
    Required in body:

    name: String
    email: String
    password: String
    """
    data = request.get_json(force=True)
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if name == "" or email == "" or password == "":
        abort(400, "Cannot have empty fields for user")

    user = User.query.filter_by(email=email).first()
    if user is not None:
        abort(400, "Account already exists with this email")

    new_user = User(name=name, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.serialize)


# log out an existing user
@auth.route("/logout")
@http_auth.login_required
def logout():
    # TODO: maybe implement this?
    return "Logged out successfully", 200
