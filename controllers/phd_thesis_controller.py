from flask import Blueprint, request
from init import db
from models.thesis import Thesis, Thesis_schema, Theses_schema

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
    body_data = request.get_json()
    new_thesis = Thesis(
        name=body_data.get("name"),
        grade=body_data.get("grade"),
        student_id=body_data.get("student_id"),
        degree_level_id=body_data.get("degree_level_id"),
    )
    db.session.add(new_thesis)
    db.session.commit()
    return Thesis_schema.dump(new_thesis), 201


@thesis_bp.route("/<int:thesis_id>", methods=["PUT", "PATCH"])
def update_thesis(thesis_id):
    try:
        stmt = db.select(Thesis).filter_by(id=thesis_id)
        thesis = db.session.scalar(stmt)
        body_data = request.get_json()
        if thesis:
            thesis.name = body_data.get("name") or thesis.name
            thesis.grade = body_data.get("grade") or thesis.grade
            thesis.student_id = body_data.get("student_id") or thesis.student_id
            thesis.degree_level_id = (
                body_data.get("degree_level_id") or thesis.degree_level_id
            )
            db.session.commit()
            return Thesis_schema.dump(thesis)
        else:
            return {"message": f"thesis with id {thesis_id} does not exist"}, 404
    except IntegrityError:
        return {"message": "thesis already in system"}, 409


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
