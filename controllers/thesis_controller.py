from flask import Blueprint, request
from init import db
from models.thesis import Thesis, Thesis_schema, Theses_schema
theses_bp = Blueprint("theses", __name__, url_prefix="/theses")

@theses_bp.route("/")
def get_theses():
    stmt = db.select(Thesis)
    theses_list = db.session.scalars(stmt)
    data = Theses_schema.dump(theses_list)
    return data

@theses_bp.route("/<int:thesis_id>")
def get_thesis(thesis_id):
    stmt = db.select(Thesis).filter_by(id=thesis_id)
    thesis=db.session.scalar(stmt)
    if thesis:
        data = Thesis_schema.dump(thesis)
        return data
    else:
        return{"message":f"thesis with id {thesis_id}"}

@theses_bp.route("/", methods=["POST"])
def create_thesis():
    body_data=request.get_json()
    new_thesis=Thesis(thesis_name=body_data.get("thesis_name"))
    db.session.add(new_thesis)
    db.session.commit()
    return Thesis_schema.dump(new_thesis), 201