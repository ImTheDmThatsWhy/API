from flask import Blueprint, request
from init import db 
from models.professor import Professor, professors_schemas, professor_schema, professors_schema
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

professors_bp= Blueprint("professors",__name__,url_prefix="/professors")

@professors_bp.route("/")
def get_professors():
    stmt = db.select(Professor)
    professors_list = db.session.scalars(stmt)
    data = professors_schema.dump(professors_list)
    return data 
@professors_bp.route("/<int:professor_id>")
def get_professor(professor_id):
    stmt = db.select(Professor).filter_by(id=professor_id)
    professor = db.session.scalar(stmt)
    if professor:
        data = professor_schema.dump(professor)
        return data
    else:
        return {"message":f"professor with id {professor_id} does not exist"}, 404

@professors_bp.route("/", methods=["POST"])
def create_professor():
    try:
        body_data = request.get_json()
        new_professor=Professor(
            name=body_data.get("name"),
            phone=body_data.get("phone"),
            email=body_data.get("email"),
            faculty_id=body_data.get("faculty_id")
        )
        db.session.add(new_professor)
        db.session.commit()
        return professor_schema.dump(new_professor), 201
    except IntegrityError as err:
        print (err.orig.pgcode)
        if err.orig.pgcode ==errorcodes.NOT_NULL_VIOLATION:
            return {"message": f"Field {err.orig.diag.column_name} required "}, 409
        
        if err.orig.pgcode==errorcodes.UNIQUE_VIOLATION:
            return{"messgae":"email address already in use"}, 409
        
    
@professors_bp.route("/<int:professor_id>", methods=["PUT", "PATCH"])
def update_professor(professor_id):
    try:
        stmt = db.select(Professor).filter_by(id=professor_id)
        professor = db.session.scalar(stmt)
        body_data = request.get_json()
   
        if professor:
            professor.name = body_data.get("name") or professor.name
            professor.phone = body_data.get("phone")
            professor.email = body_data.get("email") or professor.email
            professor.faculty_id = body_data.get("faculty_id") or professor.faculty_id
            db.session.commit()
            return professor_schema.dump(professor)
        else:
            return {"message": f"Professor with id {professor_id} does not exist"}, 404
    
    except IntegrityError:
        return {"message": "Email address already in use"}, 409

@professors_bp.route("/<int:professor_id>", methods=["Delete"])
def delete_professor(professor_id):
    stmt=db.select(Professor).filter_by(id=professor_id)
    professor=db.session.scalar(stmt)
    if professor: 
        db.session.delete(professor)
        db.session.commit()
        return{"messgae":f"professor with {professor_id} deleted"}
    else:
        return {"message":f"professor with {professor_id} does not exist"}, 404
