from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from src.users.schemas import UserSchema

from commons.pagination import paginate
from extensions import db
from models.user import User

user_app = Blueprint("users", __name__)


@user_app.route("", methods=["GET", "POST"])
def list_user_view():
    if request.method == "GET":
        schema = UserSchema(many=True)
        query = User.query
        return paginate(query, schema)
    if request.method == "POST":
        schema = UserSchema()
        user = schema.load(request.json)
        db.session.add(user)
        db.session.commit()
        return {"msg": "user created", "user": schema.dump(user)}, 201


@user_app.route("/<int:user_id>", methods=["GET", "PUT", "DELETE"])
def user_view(user_id):
    if request.method == "GET":
        schema = UserSchema()
        user = User.query.get_or_404(user_id)
        return {"user": schema.dump(user)}

    if request.method == "PUT":
        schema = UserSchema(partial=True)
        user = User.query.get_or_404(user_id)
        user = schema.load(request.json, instance=user)
        db.session.commit()
        return {"msg": "user updated", "user": schema.dump(user)}

    if request.method == "DELETE":
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"msg": "user deleted"}


@user_app.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    return jsonify(e.messages), 400
