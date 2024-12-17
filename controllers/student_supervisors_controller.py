from flask import Blueprint, request
from init import db
from models.student_supervisors import Student_supervisor, student_supervisor_schema, student_supervisors_schema
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

student_supervisors_bp= Blueprint("student_supervisors", __name__, url_prefix="/student_supervisors")

@student_supervisors_bp.route("/")
def get_student_supervisors():
    stmt = db.select(Student_supervisor)
    student_supervisor_list = db.session.scalars(stmt)
    data = student_supervisors_schema.dump(student_supervisor_list)
    return data

@student_supervisors_bp("/<int:student_supervisor_id")
def get_student_supervisor(student_supervisors_id):
    stmt = db.select(Student_supervisor).filter_by(id=student_supervisors_id)
    student_supervisors_list = db.session.scalars(stmt)
    if student_supervisors_list:
        data=student_supervisor_schema.dump(student_supervisors_list)
        return data
    else:
        return{"message":f"student_supervisor with id {student_supervisors_id} does not exist"}
        