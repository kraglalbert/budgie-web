import datetime
from flask import Flask, jsonify, request, abort, make_response
from . import main
from .. import db
from app.models import User, Transaction


# get all users
@main.route("/users", methods=["GET"])
def users():
    users = User.query.all()
    return jsonify(User.serialize_list(users))


# get user by username
@main.route("/user/<username>", methods=["GET"])
def get_user_by_username(username):
    user = User.query.filter_by(username=username).first()
    if user == None:
        abort(404)
    return jsonify(user.serialize)


# create a new user
@main.route("/users/create", methods=["POST"])
def create_user():
    data = request.get_json(force=True)
    name = data.get("name")
    username = data.get("username")
    password = data.get("password")

    new_user = User(name=name, username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.serialize)


# get all transactions
@main.route("/transactions", methods=["GET"])
def transactions():
    transactions = Transaction.query.all()
    return jsonify(Transaction.serialize_list(transactions))


# get all transactions for user
@main.route("/transactions/<int:user_id>", methods=["GET"])
def transactions_for_user(user_id):
    transactions = Transaction.query.filter_by(user_id=user_id).all()
    return jsonify(Transaction.serialize_list(transactions))


# get all transactions for user for specified month and year
@main.route("/transactions/<int:user_id>/<int:year>/<int:month>", methods=["GET"])
def transactions_for_user_month(user_id, year, month):
    transactions = Transaction.query.filter_by(user_id=user_id).all()
    result = []
    for t in transactions:
        date = t.date
        if date.year == year and date.month == month:
            result.append(t)
    return jsonify(Transaction.serialize_list(result))


# get a transaction by ID
@main.route("/transaction/<int:id>", methods=["GET"])
def get_transaction(id):
    t = Transaction.query.filter_by(id=id).first()
    if t == None:
        abort(404)
    return jsonify(t.serialize)


# create new transaction
@main.route("/transaction/create", methods=["POST"])
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


# update a transaction by ID
@main.route("/transaction/update/<int:id>", methods=["PUT"])
def update_transaction(id):
    data = request.get_json(force=True)
    title = data.get("title")
    source = data.get("source")
    amount = data.get("amount")

    year = data.get("year")
    month = data.get("month")
    day = data.get("day")

    date = datetime.datetime(int(year), int(month), int(day))

    t = Transaction.query.filter_by(id=id).first()
    t.title = title
    t.source = source
    t.amount = amount
    t.date = date

    db.session.add(t)
    db.session.commit()

    return jsonify(t.serialize)


# delete a transaction by ID
@main.route("/transaction/delete/<int:id>", methods=["DELETE"])
def delete_transaction(id):
    data = request.get_json(force=True)
    t = Transaction.query.filter_by(id=id).first()

    db.session.delete(t)
    db.session.commit()

    return jsonify(t.serialize)

@main.errorhandler(404)
def page_not_found(e):
    return "404 - Page not found!", 404

@main.errorhandler(500)
def internal_server_error(e):
    return "500 - Internal server error!", 500