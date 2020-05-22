import datetime
from flask import Flask, jsonify, request, abort, make_response
from . import auth
from .. import db
from app.models import User, Transaction, TransactionMonth
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    jwt_refresh_token_required,
    create_refresh_token,
    get_jwt_identity,
    set_access_cookies,
    set_refresh_cookies,
    unset_jwt_cookies,
)

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
        # create the tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        resp = jsonify({"user": user.serialize})
        set_access_cookies(resp, access_token)
        set_refresh_cookies(resp, refresh_token)

        return resp
    return "Wrong email or password!", 400


# check if token is valid and return user
@auth.route("/token/refresh", methods=["POST"])
@jwt_refresh_token_required
def refresh_token():
    # create the new access token
    current_user_id = get_jwt_identity()
    access_token = create_access_token(identity=current_user_id)

    user = User.query.filter_by(id=current_user_id).first()

    # set the JWT access cookie in the response
    resp = jsonify({"user": user.serialize})
    set_access_cookies(resp, access_token)

    return resp


# register a new user
@auth.route("/register", methods=["POST"])
def register():
    """
    Required in body:

    name: String
    email: String
    password: String
    default_currency: String
    """
    data = request.get_json(force=True)
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    default_currency = data.get("default_currency")

    if name is None or email is None or password is None or default_currency is None:
        abort(400, "Cannot have empty fields for user")

    user = User.query.filter_by(email=email).first()
    if user is not None:
        abort(400, "Account already exists with this email")

    new_user = User(
        name=name, email=email, password=password, default_currency=default_currency
    )
    db.session.add(new_user)
    db.session.commit()

    # create the tokens
    access_token = create_access_token(identity=new_user.id)
    refresh_token = create_refresh_token(identity=new_user.id)

    resp = jsonify({"user": new_user.serialize})
    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)

    return resp


# change password for existing user
@auth.route("/change-password", methods=["POST"])
@jwt_required
def change_password():
    """
    Required in body:

    old_password: String
    new_password: String
    """
    data = request.get_json(force=True)
    old_password = data.get("old_password")
    new_password = data.get("new_password")

    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()

    if user.change_password(old_password, new_password):
        return "Password changed successfully", 200
    else:
        return "Failed to change password", 400


# log out an existing user
@auth.route("/logout", methods=["POST"])
@jwt_required
def logout():
    resp = jsonify("Logged out successfully")
    unset_jwt_cookies(resp)
    return resp
