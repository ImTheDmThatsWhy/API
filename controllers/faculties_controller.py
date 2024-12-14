from flask import Blueprint, request
from init import db
from models.faculty import Faculty, faculties_schema, faculty_schema
from sqlalchemy.exc import IntegrityError

faculties_bp = Blueprint("faculties", __name__, url_prefix="/faculties")


@faculties_bp.route("/")
def get_faculties():
    stmt = db.select(Faculty)
    faculties_list = db.session.scalars(stmt)
    data = faculties_schema.dump(faculties_list)
    return data

@faculties_bp.route("/<int:faculty_id>")
def get_faculty(faculty_id):
    stmt = db.select(Faculty).filter_by(id=faculty_id)
    faculty = db.session.scalar(stmt)
    if faculty:
        data = faculty_schema.dump(faculty)
        return data
    else:
        return {"message": f"faculty with id{faculty_id} not found"}, 404

@faculties_bp.route("/", methods=["POST"])
def create_faculty():
    body_data = request.get_json()
    new_faculty = Faculty(
        faculty_name=body_data.get("faculty_name")
        )
    db.session.add(new_faculty)
    db.session.commit()
    return faculty_schema.dump(new_faculty), 201

@faculties_bp.route("/<int:faculty_id>", methods=["PUT", "PATCH"])
def update_faculty(faculty_id):
    try:
        stmt = db.select(Faculty).filter_by(id=faculty_id)
        faculty = db.session.scalar(stmt)
        body_data = request.get_json()
        if faculty:
            faculty.street_number = (body_data.get("faculty_name") or faculty.faculty_name)
            db.session.commit()
            return faculty_schema.dump(faculty)
        else:
            return {"message": f"faculty with id{faculty_id} does not exist"}, 404
    except IntegrityError:
        return {"message": "faculty already in system"}, 409