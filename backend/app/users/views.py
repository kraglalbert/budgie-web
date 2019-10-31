import datetime
from flask import Flask, jsonify, request, abort, make_response
from flask_login import login_required, current_user
from sqlalchemy import extract
from . import users
from .. import db
from app.models import User, Transaction, TransactionMonth

# get all users
@users.route("", methods=["GET"])
@login_required
def get_all_users():
    users = User.query.all()
    return jsonify(User.serialize_list(users))


# get user by ID
@users.route("/<int:user_id>", methods=["GET"])
@login_required
def get_user_by_id(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user == None:
        abort(404, "No user found with specified ID")
    return jsonify(user.serialize)


# get user by email
@users.route("/<email>", methods=["GET"])
@login_required
def get_user_by_email(email):
    user = User.query.filter_by(email=email).first()
    if user == None:
        abort(404, "No user found with specified email")
    return jsonify(user.serialize)


# set a user's monthly budget
@users.route("/<int:user_id>/set-budget", methods=["PUT"])
@login_required
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
