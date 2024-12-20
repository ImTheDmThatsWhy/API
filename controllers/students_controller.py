from flask import Blueprint, request
from init import db
from models.student import Student, students_schema, student_schema
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from marshmallow import ValidationError
import re

students_bp = Blueprint("students", __name__, url_prefix="/students")


@students_bp.route("/")
def get_students():
    stmt = db.select(Student)
    students_list = db.session.scalars(stmt)
    data = students_schema.dump(students_list)
    return data


@students_bp.route("/<int:student_id>")
def get_student(student_id):
    stmt = db.select(Student).filter_by(id=student_id)
    student = db.session.scalar(stmt)
    if student:
        data = student_schema.dump(student)
        return data
    else:
        return {"message": f"Student with id {student_id} does not exist"}, 404


@students_bp.route("/", methods=["POST"])
def create_student():
    try:
        body_data = student_schema.load(request.get_json())
        # while True:
        phone=body_data.get("phone")
            # combo_phone= re.search("^[1-9()])*$", phone)
        if len(phone.strip())<8:
            return{"message":"phone number must have at least 8 numbers"}
        # if combo_phone:
        #     print("phone number accepted")
        #     break
        # else:
        #     print("phone number incorrect only numbers and brackets accepted")

        new_student = Student(
            name=body_data.get("name"),
            phone=phone,
            email=body_data.get("email"),
            address_id=body_data.get("address_id"),
        )
        db.session.add(new_student)
        db.session.commit()
        return student_schema.dump(new_student), 201
    except IntegrityError as err:
        print(err.orig.pgcode)
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message": f"Field {err.orig.diag.column_name} required "}, 409

        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"message": f"email address or phone already in use"}, 409
    except ValidationError as err:
        return {"message": "Invalid fields", "errors": err.messages}, 400


@students_bp.route("/<int:student_id>", methods=["PUT", "PATCH"])
def update_student(student_id):
    try:
        stmt = db.select(Student).filter_by(id=student_id)
        student = db.session.scalar(stmt)
        body_data = request.get_json()
        phone=body_data.get("phone")
        if len(phone.strip())<8:
            return{"message":"phone number must have at least 8 numbers"}

        if student:
            student.name = body_data.get("name") or student.name
            student.phone = body_data.get("phone") or student.phone
            student.email = body_data.get("email") or student.email
            student.address_id = body_data.get("address_id") or student.address_id
            db.session.commit()
            return student_schema.dump(student)
        else:
            return {"message": f"Student with id {student_id} does not exist"}, 404

    except IntegrityError:
        return {"message": "Email address or phone number is already in use"}, 409
    except ValidationError as err:
        return {"message": "Invalid fields", "errors": err.messages}, 400



@students_bp.route("/<int:student_id>", methods=["Delete"])
def delete_student(student_id):
    try:
        stmt = db.select(Student).filter_by(id=student_id)
        student = db.session.scalar(stmt)
        if student:
            db.session.delete(student)
            db.session.commit()
            return {"message": f"student with id {student_id} deleted"}
        else:
            return {"message": f"student with id {student_id} does not exist"}, 404
    except IntegrityError:
        return {
            "message": f"student with id {student_id} is linked to a professor and cannot be deleted"
        }, 409
