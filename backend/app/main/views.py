from flask import Flask, jsonify
from . import main
from .. import db
from app.models import User, Transaction


@main.route("/")
def index():
    return "<h1>HELLO</h1>"


# get all users
@main.route("/users")
def users():
    users = User.query.all()
    return jsonify(User.serialize_list(users))


# get all transcations
@main.route("/transactions")
def transactions():
    return jsonify(res=Transaction.query.all())
