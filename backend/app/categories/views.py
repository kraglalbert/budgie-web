from flask import Flask, jsonify, request, abort, make_response
from . import categories
from .. import db
from app.models import Category
from flask_jwt_extended import jwt_required

# get all categories for user
@categories.route("/user/<int:user_id>", methods=["GET"])
@jwt_required
def get_categories_for_user(user_id):
    categories = Category.query.filter_by(user_id=user_id).all()
    return jsonify(Category.serialize_list(categories))


# create new category
@categories.route("", methods=["POST"])
@jwt_required
def create_category():
    body = request.get_json(force=True)
    name = body.get("name")
    user_id = int(body.get("user_id"))

    new_category = Category(name=name, user_id=user_id, transactions=[])
    db.session.add(new_category)
    db.session.commit()

    return jsonify(new_category.serialize)


# update existing category
@categories.route("/<int:id>", methods=["PUT"])
@jwt_required
def update_category(id):
    body = request.get_json(force=True)
    name = body.get("name")
    if name is None or name == "":
        abort(400, "Category name cannot be empty")

    category = Category.query.filter_by(id=id).first()
    if category is None:
        abort(400, "No category found with specified ID")

    category.name = name

    db.session.add(category)
    db.session.commit()

    return jsonify(category.serialize)


# delete existing category
@categories.route("/<int:id>", methods=["DELETE"])
@jwt_required
def delete_category(id):
    category = Category.query.filter_by(id=id).first()
    if category is None:
        abort(400, "No category found with specified ID")

    db.session.delete(category)
    db.session.commit()

    return jsonify(category.serialize)
