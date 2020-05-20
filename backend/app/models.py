import json
import base64
from . import db
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    monthly_budget = db.Column(db.Integer)  # amount in cents
    default_currency = db.Column(db.String(3))  # 3-letter currency code
    categories = db.relationship("Category", backref="users", lazy=True)
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
            "default_currency": self.default_currency
            if self.default_currency is not None
            else "",
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


class Transaction(db.Model):
    __tablename__ = "transactions"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    source = db.Column(db.String(64), nullable=False)
    # amount in cents
    amount = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    currency = db.Column(db.String(3), nullable=False)  # 3-letter currency code
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    transaction_month_id = db.Column(
        db.Integer, db.ForeignKey("transaction_months.id"), nullable=False
    )

    @property
    def serialize(self):
        """Return object data in serializeable format"""
        category = None
        if self.category_id is not None:
            category = Category.query.filter_by(id=self.category_id).first()

        return {
            "id": self.id,
            "title": self.title,
            "source": self.source,
            "amount": self.amount,
            "date": self.date,
            "currency": self.currency,
            "category": category.name if category is not None else "None",
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
            "transactions": Transaction.serialize_list(self.transactions),
        }

    @staticmethod
    def serialize_list(transaction_months):
        json_transactions_months = []
        for tm in transaction_months:
            json_transactions_months.append(tm.serialize)
        return json_transactions_months

    def __repr__(self):
        return "<TransactionMonth %r>" % self.title


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    transactions = db.relationship("Transaction", backref="categories", lazy=True)

    @property
    def serialize(self):
        """Return object data in serializeable format"""
        return {
            "id": self.id,
            "name": self.name,
            "user_id": self.user_id,
            "transactions": Transaction.serialize_list(self.transactions),
        }

    @staticmethod
    def serialize_list(categories):
        json_categories = []
        for c in categories:
            json_categories.append(c.serialize)
        return json_categories

    def __repr__(self):
        return "<Category %r>" % self.name
