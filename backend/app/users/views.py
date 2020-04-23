import datetime
import re
from flask import Flask, jsonify, request, abort, make_response
from sqlalchemy import extract
from . import users
from .. import db, http_auth
from app.models import User, Transaction, TransactionMonth

# get all users
@users.route("", methods=["GET"])
@http_auth.login_required
def get_all_users():
    users = User.query.all()
    return jsonify(User.serialize_list(users))


# get user by ID
@users.route("/<int:user_id>", methods=["GET"])
@http_auth.login_required
def get_user_by_id(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        abort(404, "No user found with specified ID")
    return jsonify(user.serialize)


# get user by email
@users.route("/<email>", methods=["GET"])
@http_auth.login_required
def get_user_by_email(email):
    user = User.query.filter_by(email=email).first()
    if user is None:
        abort(404, "No user found with specified email")
    return jsonify(user.serialize)


# update a user's settings (monthly budget, default currency)
@users.route("/<int:user_id>/settings", methods=["PUT"])
@http_auth.login_required
def update_user_settings(user_id):
    data = request.get_json(force=True)

    try:
        monthly_budget = int(data.get("monthly_budget"))
    except TypeError:
        monthly_budget = None

    default_currency = data.get("default_currency")

    if monthly_budget is None or default_currency is None:
        abort(400, "Must give values for monthly budget and default currency")

    if monthly_budget < 0:
        abort(400, "Monthly budget cannot be negative")

    if len(default_currency) != 3 or re.match("[A-Z]{3}", default_currency) is None:
        abort(400, "Default currency must be in 3-letter currency code format")

    user = User.query.filter_by(id=user_id).first()
    if user is None:
        abort(404, "No user found with specified ID")

    user.monthly_budget = monthly_budget
    user.default_currency = default_currency

    db.session.add(user)
    db.session.commit()
    return jsonify(user.serialize)
