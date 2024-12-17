from flask import Blueprint, request
from init import db
from models.degree_level import Degree_level, degree_schema, degrees_schema
from sqlalchemy.exc import IntegrityError

degree_levels_bp = Blueprint("degree_levels", __name__, url_prefix="/degree_levels")


@degree_levels_bp.route("/")
def get_degree_levels():
    stmt = db.select(Degree_level)
    degrees_list = db.session.scalars(stmt)
    data = degrees_schema.dump(degrees_list)
    return data


@degree_levels_bp.route("/<int:degree_level_id>")
def get_degree_level(degree_level_id):
    stmt = db.select(Degree_level).filter_by(id=degree_level_id)
    degree_level = db.session.scalar(stmt)
    if degree_level:
        data = degree_schema.dump(degree_level)
        return data
    else:
        return {"message": f"degree_level with id{degree_level_id} not found"}, 404


@degree_levels_bp.route("/", methods=["POST"])
def create_degree_level():
    body_data = request.get_json()
    new_level = Degree_level(degree_level_name=body_data.get("degree_level_name"))
    db.session.add(new_level)
    db.session.commit()
    return degree_schema.dump(new_level), 201


@degree_levels_bp.route("/<int:degree_level_id>", methods=["PUT", "PATCH"])
def update_degree_level(degree_level_id):
    try:
        stmt = db.select(Degree_level).filter_by(id=degree_level_id)
        degree_level = db.session.scalar(stmt)
        body_data = request.get_json()
        if degree_level:
            degree_level.degree_level_name = (
                body_data.get("degree_level_name") or degree_level.degree_level_name
            )
            db.session.commit()
            return degree_schema.dump(degree_level)
        else:
            return {
                "message": f"degree level with id{degree_level_id} does not exist"
            }, 404
    except IntegrityError:
        return {"message": "degree level already in system"}, 409


@degree_levels_bp.route("/<int:degree_level_id>", methods=["Delete"])
def delete_degree_level(degree_level_id):
    stmt = db.select(Degree_level).filter_by(id=degree_level_id)
    degree_level = db.session.scalar(stmt)
    if degree_level:
        db.session.delete(degree_level)
        db.session.commit()
        return {"messgage": f"degree_level with id{degree_level_id} deleted"}
    else:
        return {"message": f"degree_level with {degree_level_id} does not exist"}, 404
