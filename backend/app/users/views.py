import datetime
from flask import Flask, jsonify, request, abort, make_response
from flask_login import login_required, current_user
from sqlalchemy import extract
from . import users
from .. import db
from app.models import User, Transaction, TransactionMonth

# get all users
@users.route("", methods=["GET"])
def get_all_users():
    users = User.query.all()
    return jsonify(User.serialize_list(users))


# get user by ID
@users.route("/<int:user_id>", methods=["GET"])
def get_user_by_id(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user == None:
        abort(404, "No user found with specified ID")
    return jsonify(user.serialize)


# get user by email
@users.route("/<email>", methods=["GET"])
def get_user_by_email(email):
    user = User.query.filter_by(email=email).first()
    if user == None:
        abort(404, "No user found with specified email")
    return jsonify(user.serialize)


# create a new user
@users.route("/create", methods=["POST"])
def create_user():
    data = request.get_json(force=True)
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if name == "" or email == "" or password == "":
        abort(400, "Cannot have empty fields for user")

    new_user = User(name=name, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.serialize)


# set a user's monthly budget
@users.route("/<int:user_id>/set-budget", methods=["PUT"])
def update_user_budget(user_id):
    data = request.get_json(force=True)
    monthly_budget = int(data.get("monthly_budget"))

    if monthly_budget < 0:
        abort(400, "Monthly budget cannot be negative")

    user = User.query.filter_by(id=user_id).first()
    if user == None:
        abort(404, "No user found with specified ID")

    user.monthly_budget = monthly_budget

    db.session.add(user)
    db.session.commit()
    return jsonify(user.serialize)
