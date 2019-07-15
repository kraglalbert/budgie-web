import datetime
from flask import Flask, jsonify, request, abort
from . import main
from .. import db
from app.models import User, Transaction
from werkzeug.security import generate_password_hash


# get all users
@main.route("/users")
def users():
    users = User.query.all()
    return jsonify(User.serialize_list(users))


# get user by username
@main.route("/user/<username>")
def get_user_by_username(username):
    user = User.query.filter_by(username=username).first()
    if user == None:
        abort(404)
    return jsonify(user.serialize)


# create a new user
@main.route("/users/create", methods=["POST"])
def create_user():
    data = request.get_json(force=True)
    name = data["name"]
    username = data["username"]
    password = generate_password_hash(data["password"])

    new_user = User(name=name, username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.serialize)


# get all transactions
@main.route("/transactions")
def transactions():
    return jsonify(res=Transaction.query.all())


# create new transaction
@main.route("/transactions/create", methods=["POST"])
def create_transaction():
    data = request.get_json(force=True)
    title = data.get("title")
    source = data.get("source")
    amount = data.get("amount")
    username = data.get("username")

    year = data.get("year")
    month = data.get("month")
    day = data.get("day")

    date = datetime.datetime(int(year), int(month), int(day))

    user = User.query.filter_by(username=username).first()

    new_transaction = Transaction(
        title=title, source=source, amount=amount, user_id=user.id, date=date
    )
    db.session.add(new_transaction)
    db.session.commit()

    return jsonify(new_transaction.serialize)

