from flask import Blueprint, request
from init import db
from models.thesis import Thesis, Thesis_schema, Theses_schema
from marshmallow import ValidationError

thesis_bp = Blueprint("thesis", __name__, url_prefix="/thesis")
from sqlalchemy.exc import IntegrityError


@thesis_bp.route("/")
def get_theses():
    stmt = db.select(Thesis)
    theses_list = db.session.scalars(stmt)
    data = Theses_schema.dump(theses_list)
    return data


@thesis_bp.route("/<int:thesis_id>")
def get_thesis(thesis_id):
    stmt = db.select(Thesis).filter_by(id=thesis_id)
    thesis = db.session.scalar(stmt)
    if thesis:
        data = Thesis_schema.dump(thesis)
        return data
    else:
        return {"message": f"thesis with id {thesis_id} not found"}, 404


@thesis_bp.route("/", methods=["POST"])
def create_thesis():
    try:
        body_data = Thesis_schema.load(request.get_json())
        new_thesis = Thesis(
            name=body_data.get("name"),
            status_id=body_data.get("status_id"),
            student_id=body_data.get("student_id"),)
        db.session.add(new_thesis)
        db.session.commit()
        return Thesis_schema.dump(new_thesis), 201
    except IntegrityError:
        return {"message": f"student is already in the system or does not exist"}, 409
    except ValidationError as err:
        return {"message": "Invalid fields", "errors": err.messages}, 400


@thesis_bp.route("/<int:thesis_id>", methods=["PUT", "PATCH"])
def update_thesis(thesis_id):
    try:
        stmt = db.select(Thesis).filter_by(id=thesis_id)
        thesis = db.session.scalar(stmt)
        body_data = request.get_json()
        if thesis:
            thesis.name = body_data.get("name") or thesis.name
            thesis.student_id = body_data.get("student_id") or thesis.student_id
            thesis.status_id = (
                body_data.get("status_id") or thesis.status_id
            )
            db.session.commit()
            return Thesis_schema.dump(thesis)
        else:
            return {"message": f"thesis with id {thesis_id} does not exist"}, 404
    except IntegrityError:
        return {"message": "status_id or student_id does not exist"}, 409


@thesis_bp.route("/<int:thesis_id>", methods=["Delete"])
def delete_thesis(thesis_id):
    stmt = db.select(Thesis).filter_by(id=thesis_id)
    thesis = db.session.scalar(stmt)
    if thesis:
        db.session.delete(thesis)
        db.session.commit()
        return {"messgage": f"thesis with id {thesis_id} deleted"}
    else:
        return {"message": f"thesis with {thesis_id} does not exist"}, 404

