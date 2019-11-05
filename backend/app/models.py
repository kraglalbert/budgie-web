import json
import base64
from . import db, login_manager
from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    # amount in cents
    monthly_budget = db.Column(db.Integer)
    transactions = db.relationship("Transaction", backref="users", lazy=True)
    transactions_months = db.relationship(
        "TransactionMonth", backref="users", lazy=True
    )

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expiration=604800):
        s = Serializer(current_app.config["SECRET_KEY"], expiration)
        return s.dumps({"token": self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data["id"])
        return user

    @staticmethod
    def generate_test_user():
        user = User(name="Albert Kragl", email="akragl@gmail.com", password="password")
        db.session.add(user)
        db.session.commit()
        return user

    @property
    def serialize(self):
        """Return object data in serializeable format"""
        return {
            "id": self.id,
            "name": self.name,
            "password_hash": self.password_hash,
            "monthly_budget": self.monthly_budget
            if self.monthly_budget is not None
            else 0,
            "transactions": Transaction.serialize_list(self.transactions),
            "email": self.email,
        }

    @staticmethod
    def serialize_list(users):
        json_users = []
        for user in users:
            json_users.append(user.serialize)
        return json_users

    def __repr__(self):
        return "<User %r>" % self.email


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@login_manager.request_loader
def load_user_from_request(request):
    # first, try to login using the api_key url arg
    api_key = request.args.get("api_key")
    if api_key:
        user = User.verify_auth_token(api_key)
        if user:
            return user

    # next, try to login using Basic Auth
    api_key = request.headers.get("Authorization")
    print(api_key)
    if api_key:
        api_key = api_key.replace("Basic ", "", 1)
        try:
            api_key = base64.b64decode(api_key)
        except TypeError:
            pass
        user = User.verify_auth_token(api_key)
        if user:
            return user

    # finally, return None if both methods did not login the user
    return None


class Transaction(db.Model):
    __tablename__ = "transactions"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), unique=False, nullable=False)
    source = db.Column(db.String(64), nullable=False)
    # amount in cents
    amount = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    transaction_month_id = db.Column(
        db.Integer, db.ForeignKey("transaction_months.id"), nullable=False
    )

    @property
    def serialize(self):
        """Return object data in serializeable format"""
        return {
            "id": self.id,
            "title": self.title,
            "source": self.source,
            "amount": self.amount,
            "date": self.date,
            "year": self.date.year,
            "month": self.date.month,
            "day": self.date.day,
            "user_id": self.user_id,
            "transaction_month_id": self.transaction_month_id,
        }

    @staticmethod
    def serialize_list(transactions):
        json_transactions = []
        for t in transactions:
            json_transactions.append(t.serialize)
        return json_transactions

    def __repr__(self):
        return "<Transaction %r>" % self.title


class TransactionMonth(db.Model):
    __tablename__ = "transaction_months"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    transactions = db.relationship(
        "Transaction", backref="transaction_months", lazy=True
    )

    @property
    def serialize(self):
        """Return object data in serializeable format"""
        return {
            "id": self.id,
            "date": self.date,
            "year": self.date.year,
            "month": self.date.month,
            "transactions": self.transactions,
        }

    @staticmethod
    def serialize_list(transaction_months):
        json_transactions_months = []
        for tm in transaction_months:
            json_transactions_months.append(tm.serialize)
        return json_transactions_months

    def __repr__(self):
        return "<TransactionMonth %r>" % self.title
