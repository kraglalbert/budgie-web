import datetime
import re
from flask import Flask, jsonify, request, abort, make_response
from sqlalchemy import extract
from . import users
from .. import db
from app.models import User, Transaction, TransactionMonth
from flask_jwt_extended import jwt_required

# get all users
@users.route("", methods=["GET"])
@jwt_required
def get_all_users():
    users = User.query.all()
    return jsonify(User.serialize_list(users))


# get user by ID
@users.route("/id/<int:user_id>", methods=["GET"])
@jwt_required
def get_user_by_id(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        abort(404, "No user found with specified ID")
    return jsonify(user.serialize)


# get user by email
@users.route("/email/<email>", methods=["GET"])
@jwt_required
def get_user_by_email(email):
    user = User.query.filter_by(email=email).first()
    if user is None:
        abort(404, "No user found with specified email")
    return jsonify(user.serialize)


# update a user's settings (monthly budget, default currency)
@users.route("/<int:user_id>/settings", methods=["PUT"])
@jwt_required
def update_user_settings(user_id):
    data = request.get_json(force=True)

    user = User.query.filter_by(id=user_id).first()
    if user is None:
        abort(404, "No user found with specified ID")

    try:
        monthly_budget = int(data.get("monthly_budget"))
    except TypeError:
        monthly_budget = None

    try:
        monthly_budget_from_net = bool(data.get("monthly_budget_from_net"))
    except TypeError:
        monthly_budget_from_net = None

    selected_currency = data.get("selected_currency")
    primary_currency = data.get("primary_currency")

    if (
        monthly_budget is None
        and selected_currency is None
        and primary_currency is None
    ):
        abort(400, "No values given to update")

    if monthly_budget is not None:
        if monthly_budget < 0:
            abort(400, "Monthly budget cannot be negative")

        user.monthly_budget = monthly_budget

    if monthly_budget_from_net is not None:
        user.monthly_budget_from_net = monthly_budget_from_net

    if selected_currency is not None:
        if (
            len(selected_currency) != 3
            or re.match("[A-Z]{3}", selected_currency) is None
        ):
            abort(400, "Selected currency must be in 3-letter currency code format")

        user.selected_currency = selected_currency

    if primary_currency is not None:
        if len(primary_currency) != 3 or re.match("[A-Z]{3}", primary_currency) is None:
            abort(400, "Primary currency must be in 3-letter currency code format")

        user.primary_currency = primary_currency

    db.session.add(user)
    db.session.commit()
    return jsonify(user.serialize)
