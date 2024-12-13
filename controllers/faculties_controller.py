from flask import Blueprint
from init import db
from models.faculty import Faculty, faculties_schema, faculty_schema

faculties_bp = Blueprint("faculties", __name__, url_prefix="/faculties")

@faculties_bp.route("/")
def get_faculties():
    stmt = db.select(Faculty)
    faculties_list = db.session.scalars(stmt)
    data = faculties_schema.dump(faculties_list)
    return data