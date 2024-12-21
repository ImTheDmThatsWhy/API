from flask import Blueprint, request
from init import db
from models.faculty import Faculty, faculties_schema, faculty_schema
from sqlalchemy.exc import IntegrityError, ProgrammingError
from marshmallow import ValidationError
from psycopg2 import errorcodes

faculties_bp = Blueprint("faculties", __name__, url_prefix="/faculties")


@faculties_bp.route("/")
def get_faculties():
    try:
        stmt = db.select(Faculty)
        faculties_list = db.session.scalars(stmt)
        data = faculties_schema.dump(faculties_list)
        return data
    except ProgrammingError:
        return {"message": "tables need to be seeded with data"}, 400


@faculties_bp.route("/<int:faculty_id>")
def get_faculty(faculty_id):
    try:
        stmt = db.select(Faculty).filter_by(id=faculty_id)
        faculty = db.session.scalar(stmt)
        if faculty:
            data = faculty_schema.dump(faculty)
            return data
        else:
            return {"message": f"faculty with id{faculty_id} not found"}, 404
    except ProgrammingError:
        return {"message": "tables need to be seeded with data"}, 400


@faculties_bp.route("/", methods=["POST"])
def create_faculty():
    try:
        body_data = faculty_schema.load(request.get_json())
        new_faculty = Faculty(faculty_name=body_data.get("faculty_name"))
        db.session.add(new_faculty)
        db.session.commit()
        return faculty_schema.dump(new_faculty), 201
    except ValidationError as err:
        return {"message": "Invalid fields", "errors": err.messages}, 400
    except IntegrityError as err:
        print(err.orig.pgcode)
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message": f"Field {err.orig.diag.column_name} required "}, 409
    except IntegrityError:
        return {"message": "faculty already in system"}, 409


@faculties_bp.route("/<int:faculty_id>", methods=["PUT", "PATCH"])
def update_faculty(faculty_id):
    try:
        stmt = db.select(Faculty).filter_by(id=faculty_id)
        faculty = db.session.scalar(stmt)
        body_data = request.get_json()
        if faculty:
            faculty.faculty_name = body_data.get("faculty_name") or faculty.faculty_name
            db.session.commit()
            return faculty_schema.dump(faculty)
        else:
            return {"message": f"faculty with id{faculty_id} does not exist"}, 404
    except IntegrityError:
        return {"message": "faculty already in system"}, 409
    except IntegrityError as err:
        print(err.orig.pgcode)
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message": f"Field {err.orig.diag.column_name} required "}, 409
    except ValidationError as err:
        return {"message": "Invalid fields", "errors": err.messages}, 400
    except ProgrammingError:
        return {"message": "tables need to be seeded with data"}, 400


@faculties_bp.route("/<int:faculty_id>", methods=["Delete"])
def delete_faculty(faculty_id):
    try:
        stmt = db.select(Faculty).filter_by(id=faculty_id)
        faculty = db.session.scalar(stmt)
        if faculty:
            db.session.delete(faculty)
            db.session.commit()
            return {"messgage": f"faculty with id{faculty_id} deleted"}
        else:
            return {"message": f"faculty with {faculty_id} does not exist"}, 404
    except ProgrammingError:
        return {"message": "tables need to be seeded with data"}, 400
