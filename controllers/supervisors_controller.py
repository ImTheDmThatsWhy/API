from flask import Blueprint, request
from init import db
import re
from models.supervisor import (
    Supervisor,
    supervisor_schema,
    supervisors_schema,
)
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

supervisors_bp = Blueprint("supervisors", __name__, url_prefix="/supervisors")

@supervisors_bp.route("/")
def get_supervisors():
    stmt = db.select(Supervisor)
    supervisors_list = db.session.scalars(stmt)
    data = supervisors_schema.dump(supervisors_list)
    return data


@supervisors_bp.route("/<int:supervisor_id>")
def get_supervisor(supervisor_id):
    stmt = db.select(Supervisor).filter_by(id=supervisor_id)
    supervisor = db.session.scalar(stmt)
    if supervisor:
        data = supervisor_schema.dump(supervisor)
        return data
    else:
        return {"message": f"supervisor with id {supervisor_id} does not exist"}, 404


@supervisors_bp.route("/", methods=["POST"])
def create_supervisor():
    try:
        body_data = request.get_json()
        email = str(body_data.get("email"))
        email_format= re.match(r'^[a-zA-Z0-9_]+@[a-zA-Z0-9_]+.[a-zA-Z]$',email)
        if email!=email_format:
            return {"message":"invalid email address"}, 400
        name = str(body_data.get("name"))
        if len(name.strip()) == 0:
            return {"message": "Field name cannot be empty"}, 400
        new_supervisor = Supervisor(
            name=body_data.get("name"),
            phone=body_data.get("phone"),
            email=body_data.get("email"),
            faculty_id=body_data.get("faculty_id"),
        )
        db.session.add(new_supervisor)
        db.session.commit()
        return supervisor_schema.dump(new_supervisor), 201
    except IntegrityError as err:
        print(err.orig.pgcode)
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message": f"Field {err.orig.diag.column_name} required "}, 409

        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"messgae": "email address or phone number already in use"}, 409


@supervisors_bp.route("/<int:supervisor_id>", methods=["PUT", "PATCH"])
def update_supervisor(supervisor_id):
    try:
        stmt = db.select(Supervisor).filter_by(id=supervisor_id)
        supervisor = db.session.scalar(stmt)
        body_data = request.get_json()

        if supervisor:
            supervisor.name = body_data.get("name") or supervisor.name
            supervisor.phone = body_data.get("phone") or supervisor.phone
            supervisor.email = body_data.get("email") or supervisor.email
            supervisor.faculty_id = body_data.get("faculty_id") or supervisor.faculty_id
            db.session.commit()
            return supervisor_schema.dump(supervisor)
        else:
            return {"message": f"supervisor with id {supervisor_id} does not exist"}, 404

    except IntegrityError:
        return {"message": "Email address already in use"}, 409


@supervisors_bp.route("/<int:supervisor_id>", methods=["Delete"])
def delete_supervisor(supervisor_id):
    try:
        stmt = db.select(Supervisor).filter_by(id=supervisor_id)
        supervisor = db.session.scalar(stmt)
        if supervisor:
            db.session.delete(supervisor)
            db.session.commit()
            return {"messgae": f"supervisor with id {supervisor_id} deleted"}
        else:
            return {"message": f"supervisor with {supervisor_id} does not exist"}, 404
    except IntegrityError:
        return {"message": f"supervisor with {supervisor_id} is linked to a student and cannot be deleted"}, 409
