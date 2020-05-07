import datetime
from flask import Flask, jsonify, request, abort, make_response
from sqlalchemy import extract
from calendar import monthrange
from . import transactions
from .. import db, http_auth
from app.models import User, Transaction, TransactionMonth, Category

# get all transactions
@transactions.route("", methods=["GET"])
@http_auth.login_required
def get_transactions():
    transactions = Transaction.query.all()
    return jsonify(Transaction.serialize_list(transactions))


# get transactions for user
@transactions.route("/user/<int:user_id>", methods=["GET"])
@http_auth.login_required
def get_transactions_for_user(user_id):
    year = request.args.get("year")
    month = request.args.get("month")

    if year is not None and month is None:
        # get all transactions for specified year
        t_months = TransactionMonth.query.filter(
            extract("year", TransactionMonth.date) == int(year),
            TransactionMonth.user_id == user_id,
        ).all()
        if t_months is None:
            abort(400, "No transactions exist for this user in the specified year")

        transactions = []
        for t_month in t_months:
            transactions.extend(t_month.transactions)
        return jsonify(Transaction.serialize_list(transactions))

    if year is None and month is None:
        # return all transactions for user
        transactions = Transaction.query.filter_by(user_id=user_id).all()
        return jsonify(Transaction.serialize_list(transactions))

    if year is None and month is not None:
        abort(400, "Must specify a year with optional month")

    # get transactions for specified month and year
    t_month = TransactionMonth.query.filter(
        extract("year", TransactionMonth.date) == int(year),
        extract("month", TransactionMonth.date) == int(month),
        TransactionMonth.user_id == user_id,
    ).first()
    if t_month is None:
        return jsonify([])

    transactions = t_month.transactions
    return jsonify(Transaction.serialize_list(transactions))


# get transaction months for user
@transactions.route("/user/<int:user_id>/months", methods=["GET"])
@http_auth.login_required
def get_transaction_months_for_user(user_id):
    transaction_months = TransactionMonth.query.filter_by(user_id=user_id).all()
    result = []

    for t_month in transaction_months:
        total_spent = 0
        total_earned = 0
        for t in t_month.transactions:
            if t.amount > 0:
                total_earned += t.amount
            else:
                total_spent += -1 * t.amount

        t_month_summary = {
            "date": t_month.date,
            "total_earned": total_earned,
            "total_spent": total_spent,
            "net": total_earned - total_spent,
        }
        result.append(t_month_summary)

    return jsonify(result)


# get amount spent each day for specified month
@transactions.route("/user/<int:user_id>/by-day", methods=["GET"])
@http_auth.login_required
def get_amount_by_day(user_id):
    year = int(request.args.get("year"))
    month = int(request.args.get("month"))
    transaction_type = request.args.get("type")

    if year is None or month is None:
        abort(400, "Must specify month and year")

    if month < 1 or month > 12:
        abort(400, "Invalid value for month")

    # get transactions for specified month and year
    t_month = TransactionMonth.query.filter(
        extract("year", TransactionMonth.date) == int(year),
        extract("month", TransactionMonth.date) == int(month),
        TransactionMonth.user_id == user_id,
    ).first()
    if t_month is None:
        abort(400, "Transaction month does not exist for specified user")

    transactions = t_month.transactions
    if transaction_type is not None:
        if transaction_type == "spendings":
            transactions = filter(lambda t: t.amount < 0, transactions)
        elif transaction_type == "profits":
            transactions = filter(lambda t: t.amount > 0, transactions)

    # get number of days in the specified month
    num_days_tuple = monthrange(year, month)
    num_days = num_days_tuple[1]

    spendings_per_day = {}
    for i in range(1, num_days + 1):
        spendings_per_day[i] = 0

    for t in transactions:
        t_day = t.date.day
        spendings_per_day[t_day] += t.amount

    return jsonify(spendings_per_day)


# get a transaction by ID
@transactions.route("/<int:id>", methods=["GET"])
@http_auth.login_required
def get_transaction(id):
    t = Transaction.query.filter_by(id=id).first()
    if t is None:
        abort(404, "No transaction found with specified ID")
    return jsonify(t.serialize)


# create new transaction
@transactions.route("", methods=["POST"])
@http_auth.login_required
def create_transaction():
    data = request.get_json(force=True)
    title = data.get("title")
    source = data.get("source")
    amount = int(data.get("amount"))
    email = data.get("email")
    category_name = data.get("category")

    year = data.get("year")
    month = data.get("month")
    day = data.get("day")

    if (
        title == ""
        or source == ""
        or amount is None
        or email == ""
        or year is None
        or month is None
        or day is None
    ):
        abort(400, "Cannot have empty fields for transaction")

    try:
        date = datetime.datetime(int(year), int(month), int(day))
    except ValueError:
        abort(400, "Invalid date given for transaction")

    user = User.query.filter_by(email=email).first()
    if user is None:
        abort(404, "User does not exist")

    # check if transaction month exists
    t_month = TransactionMonth.query.filter(
        extract("year", TransactionMonth.date) == int(year),
        extract("month", TransactionMonth.date) == int(month),
        TransactionMonth.user_id == user.id,
    ).first()
    if t_month is None:
        # create transaction month object if it doesn't exist
        t_month = TransactionMonth(
            date=datetime.datetime(int(year), int(month), 1), user_id=user.id
        )
        db.session.add(t_month)
        db.session.commit()

    # get category object
    category_id = None
    if category_name != "None":
        category = Category.query.filter(
            Category.user_id == user.id, Category.name == category_name
        ).first()
        category_id = category.id

    new_transaction = Transaction(
        title=title,
        source=source,
        amount=amount,
        user_id=user.id,
        date=date,
        category_id=category_id,
        transaction_month_id=t_month.id,
    )
    db.session.add(new_transaction)
    db.session.commit()

    return jsonify(new_transaction.serialize)


# update a transaction by ID
@transactions.route("/<int:id>", methods=["PUT"])
@http_auth.login_required
def update_transaction(id):
    data = request.get_json(force=True)
    title = data.get("title")
    source = data.get("source")
    amount = int(data.get("amount"))

    year = data.get("year")
    month = data.get("month")
    day = data.get("day")

    if (
        title == ""
        or source == ""
        or amount is None
        or year is None
        or month is None
        or day is None
    ):
        abort(400, "Cannot have empty fields for transaction")

    try:
        date = datetime.datetime(int(year), int(month), int(day))
    except ValueError:
        abort(400, "Invalid date given for transaction")

    t = Transaction.query.filter_by(id=id).first()
    if t is None:
        abort(400, "No transaction found with specified ID")

    t.title = title
    t.source = source
    t.amount = amount
    t.date = date

    db.session.add(t)
    db.session.commit()

    return jsonify(t.serialize)


# delete a transaction by ID
@transactions.route("/<int:id>", methods=["DELETE"])
@http_auth.login_required
def delete_transaction(id):
    t = Transaction.query.filter_by(id=id).first()
    if t is None:
        abort(404, "No transaction found with specified ID")

    db.session.delete(t)
    db.session.commit()

    return jsonify(t.serialize)
