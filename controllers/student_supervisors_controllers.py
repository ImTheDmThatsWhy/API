from flask import Blueprint, request
from init import db
from models.student_supervisors import (
    Student_supervisor,
    student_supervisor_schema,
    student_supervisors_schema,
)
from sqlalchemy.exc import IntegrityError, DataError, ProgrammingError
from psycopg2 import errorcodes

student_supervisors_bp = Blueprint(
    "student_supervisors", __name__, url_prefix="/student_supervisors"
)


@student_supervisors_bp.route("/")
def get_student_supervisors():
    try:
        stmt = db.select(Student_supervisor)
        student_supervisor_list = db.session.scalars(stmt)
        data = student_supervisors_schema.dump(student_supervisor_list)
        return data
    except ProgrammingError:
        return {"message": "tables need to be seeded with data"}, 400


@student_supervisors_bp.route("/<int:student_supervisor_id>")
def get_student_supervisor(student_supervisor_id):
    try:
        stmt = db.select(Student_supervisor).filter_by(id=student_supervisor_id)
        student_supervisors_list = db.session.scalar(stmt)
        if student_supervisors_list:
            data = student_supervisor_schema.dump(student_supervisors_list)
            return data
        else:
            return {
                "message": f"student_supervisor with id {student_supervisor_id} does not exist"
            }
    except ProgrammingError:
        return {"message": "tables need to be seeded with data"}, 400


@student_supervisors_bp.route("/", methods=["POST"])
def create_student_supervisor():
    try:
        body_data = request.get_json()
        new_student_supervisor = Student_supervisor(
            student_id=body_data.get("student_id"),
            supervisor_id=body_data.get("supervisor_id"),
        )
        db.session.add(new_student_supervisor)
        db.session.commit()
        return student_supervisor_schema.dump(new_student_supervisor), 201
    except IntegrityError as err:
        print(err.orig.pgcode)
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message": f"Field {err.orig.diag.column_name} required "}, 409
    except DataError as err:
        return {"message": "student or professor_id must be entered"}, 400


@student_supervisors_bp.route("/<int:student_supervisor_id>", methods=["PUT", "PATCH"])
def update_student_supervisor(student_supervisor_id):

    stmt = db.select(Student_supervisor).filter_by(id=student_supervisor_id)
    student_supervisor = db.session.scalar(stmt)
    body_data = request.get_json()
    try:
        if student_supervisor:
            student_supervisor.student_id = (
                body_data.get("student_id") or student_supervisor.student_id
            )
            student_supervisor.supervisor_id = (
                body_data.get("supervisor_id") or student_supervisor.supervisor_id
            )
            db.session.commit()
            return student_supervisor_schema.dump(student_supervisor)
        else:
            return {
                "message": f"Student with id {student_supervisor_id} does not exist"
            }, 404
    except IntegrityError as err:
        print(err.orig.pgcode)
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message": f"Field {err.orig.diag.column_name} required "}, 409
    except DataError as err:
        return {"message": "student or professor_id must be entered"}, 400
    except ProgrammingError:
        return {"message": "tables need to be seeded with data"}, 400


@student_supervisors_bp.route("/<int:student_supervisor_id>", methods=["Delete"])
def delete_student(student_supervisor_id):
    try:
        stmt = db.select(Student_supervisor).filter_by(id=student_supervisor_id)
        student_supervisor = db.session.scalar(stmt)
        if student_supervisor:
            db.session.delete(student_supervisor)
            db.session.commit()
            return {
                "messgae": f"student_supervisor with {student_supervisor_id} deleted"
            }
        else:
            return {
                "message": f"student_supervisor with {student_supervisor_id} does not exist"
            }, 404
    except ProgrammingError:
        return {"message": "tables need to be seeded with data"}, 400
