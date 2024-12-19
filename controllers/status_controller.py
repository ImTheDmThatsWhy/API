from flask import Blueprint, request
from init import db
from models.status import Status, status_schema, statuses_schema
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

status_bp = Blueprint("status", __name__, url_prefix="/status")


@status_bp.route("/")
def get_statuses():
    stmt = db.select(Status)
    status_list = db.session.scalars(stmt)
    data = statuses_schema.dump(status_list)
    return data


@status_bp.route("/<int:status_id>")
def get_status(status_id):
    stmt = db.select(Status).filter_by(id=status_id)
    status = db.session.scalar(stmt)
    if status:
        data = status_schema.dump(status)
        return data
    else:
        return {"message": f"status with id{status_id} not found"}, 404


@status_bp.route("/", methods=["POST"])
def create_status():
    try:
        body_data = request.get_json()
        new_status = Status(status_name=body_data.get("status_name"))
        db.session.add(new_status)
        db.session.commit()
        return status_schema(new_status), 201
    except IntegrityError as err:
        print(err.orig.pgcode)
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message": f"Field {err.orig.diag.column_name} required "}, 409


@status_bp.route("/<int:status_id>", methods=["PUT", "PATCH"])
def update_status(status_id):
    try:
        stmt = db.select(Status).filter_by(id=status_id)
        status = db.session.scalar(stmt)
        body_data = request.get_json()
        if status:
            status.status_name = body_data.get("status_name") or status.status_name
            db.session.commit()
            return status_schema.dump(status)
        else:
            return {"message": f"status with id {status_id} does not exist"}, 404
    except IntegrityError:
        return {"message": "status already in system"}, 409


@status_bp.route("/<int:status_id>", methods=["Delete"])
def delete_status(status_id):
    try:
        stmt = db.select(Status).filter_by(id=status_id)
        status = db.session.scalar(stmt)
        if status:
            db.session.delete(status)
            db.session.commit()
            return {"messgage": f"status with id{status_id} deleted"}
        else:
            return {"message": f"status with {status_id} does not exist"}, 404
    except IntegrityError:
        return {"message": f"status with {status_id} is linked to a thesis and cannot be deleted"}, 409