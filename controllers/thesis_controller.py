from flask import Blueprint, request
from init import db
from models.thesis import Thesis, Thesis_schema, Theses_schema
theses_bp = Blueprint("theses", __name__, url_prefix="/theses")
from sqlalchemy.exc import IntegrityError

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

@theses_bp.route("/<int:thesis_id", methods=["PUT", "PATCH"])
def update_thesis(thesis_id):
    try:
        stmt=db.select(Thesis).filter_by(id=thesis_id)
        thesis=db.session.scalar(stmt)
        body_data=request.get_json()
        if thesis:
            thesis.thesis_name=body_data.get("thesis_name") or thesis.thesis_name
            db.session.commit()
            return Thesis_schema.dump(thesis)
        else:
            return {"message": f"thesis with id {thesis_id} does not exist"}, 404
    except IntegrityError:
        return {"message": "thesis already in system"}, 409
    
@theses_bp.route("/<int:theses_id>", methods=["Delete"])
def delete_thesis(thesis_id):
    stmt = db.select(Thesis).filter_by(id=thesis_id)
    thesis = db.session.scalar(stmt)
    if thesis:
        db.session.delete(thesis)
        db.session.commit()
        return {"messgage": f"thesis with id {thesis_id} deleted"}
    else:
        return {"message": f"thesis with {thesis_id} does not exist"}, 404
