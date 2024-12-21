from flask import Blueprint, request
from init import db
from models.address import Address, addresses_schema, address_schema
from sqlalchemy.exc import IntegrityError, DataError,ProgrammingError
from marshmallow import ValidationError
from psycopg2 import errorcodes
addresses_bp = Blueprint("addresses", __name__, url_prefix="/addresses")


@addresses_bp.route("/")
def get_addresses():
    try:
        stmt = db.select(Address)
        addresses_list = db.session.scalars(stmt)
        data = addresses_schema.dump(addresses_list)
        return data
    except ProgrammingError:
        return {"message":"tables need to be seeded with data"},400


@addresses_bp.route("/<int:address_id>")
def get_address(address_id):
    try:
        stmt = db.select(Address).filter_by(id=address_id)
        address = db.session.scalar(stmt)
        if address:
            data = address_schema.dump(address)
            return data
        else:
            return {"message": f"address with id{address_id} not found"}, 404
    except ProgrammingError:
        return {"message":"tables need to be seeded with data"},400


@addresses_bp.route("/", methods=["POST"])
def create_address():
    try:
        body_data = request.get_json()
        stmt = db.select(Address)
        address = db.session.scalars(stmt)
        postcode=body_data.get("postcode")
        
        if len(postcode.strip())<4:
            return {"message":"postcode must be 4 numbers"}
        if len(postcode.strip())>4:
            return {"message":"postcode must be 4 numbers"}
        new_address = Address(
            street_number=body_data.get("street_number"),
            street=body_data.get("street"),
            suburb=body_data.get("suburb"),
            postcode=postcode,
            state=body_data.get("state"),
        )
        if new_address == address:
            raise IntegrityError
        ("This address already exists"), 409
        db.session.add(new_address)
        db.session.commit()
        return address_schema.dump(new_address), 201
    except IntegrityError as e:
        print(e)
    except ValidationError as err:
        return {"message": "Invalid fields", "errors": err.messages}, 400
    except IntegrityError as err:
        print(err.orig.pgcode)
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message": f"Field {err.orig.diag.column_name} required "}, 409
    except DataError as err:
        return {"message":"postcode or street number must be entered"}, 400

@addresses_bp.route("/<int:address_id>", methods=["PUT", "PATCH"])
def update_address(address_id):
    try:
        stmt = db.select(Address).filter_by(id=address_id)
        address = db.session.scalar(stmt)
        body_data = request.get_json()
        if address:
            address.street_number = body_data.get("street_number") or address.street_number
            address.street = body_data.get("street") or address.street
            address.suburb = body_data.get("suburb") or address.suburb
            address.postcode = body_data.get("postcode") or address.postcode
            address.state = body_data.get("state") or address.state
            db.session.commit()
            return address_schema.dump(address)
        else:
            return {"message": f"address with id{address_id} does not exist"}, 404
    except ValidationError as err:
        return {"message": "Invalid fields", "errors": err.messages}, 400
    except IntegrityError as err:
        print(err.orig.pgcode)
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message": f"Field {err.orig.diag.column_name} required "}, 409
    except DataError as err:
        return {"message":"postcode or street number must be entered"}, 400
    except ProgrammingError:
        return {"message":"tables need to be seeded with data"},400


# except IntegrityError:
#     return {"message": "address already in system"}, 409


@addresses_bp.route("/<int:address_id>", methods=["Delete"])
def delete_address(address_id):
    try:
        stmt = db.select(Address).filter_by(id=address_id)
        address = db.session.scalar(stmt)
        if address:
            db.session.delete(address)
            db.session.commit()
            return {"messgage": f"address with id{address_id} deleted"}
        else:
            return {"message": f"address with {address_id} does not exist"}, 404
    except IntegrityError:
        return {
            "message": f"address with id {address_id} is linked to a student and cannot be deleted"
        }, 409
    except ProgrammingError:
        return {"message":"tables need to be seeded with data"},400
