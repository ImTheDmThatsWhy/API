from flask import Blueprint, request
from init import db
from models.address import Address, addresses_schema, address_schema
from sqlalchemy.exc import IntegrityError

addresses_bp = Blueprint("addresses", __name__, url_prefix="/addresses")


@addresses_bp.route("/")
def get_addresses():
    stmt = db.select(Address)
    addresses_list = db.session.scalars(stmt)
    data = addresses_schema.dump(addresses_list)
    return data


@addresses_bp.route("/<int:address_id>")
def get_address(address_id):
    stmt = db.select(Address).filter_by(id=address_id)
    address = db.session.scalar(stmt)
    if address:
        data = address_schema.dump(address)
        return data
    else:
        return {"message": f"address with id{address_id} not found"}, 404


@addresses_bp.route("/", methods=["POST"])
def create_address():
    body_data = request.get_json()
    new_address = Address(
        street_number=body_data.get("street_number"),
        street=body_data.get("street"),
        suburb=body_data.get("suburb"),
        postcode=body_data.get("postcode"),
        state=body_data.get("state"),
    )
    db.session.add(new_address)
    db.session.commit()
    return address_schema.dump(new_address), 201


@addresses_bp.route("/<int:address_id>", methods=["PUT", "PATCH"])
def update_address(address_id):
    try:
        stmt = db.select(Address).filter_by(id=address_id)
        address = db.session.scalar(stmt)
        body_data = request.get_json()
        if address:
            address.street_number = (
                body_data.get("street_number") or address.street_number
            )
            address.street = body_data.get("street") or address.street
            address.suburb = body_data.get("suburb") or address.suburb
            address.postcode = body_data.get("postcode") or address.postcode
            address.state = body_data.get("state") or address.state
            db.session.commit()
            return address_schema.dump(address)
        else:
            return {"message": f"address with id{address_id} does not exist"}, 404
    except IntegrityError:
        return {"message": "address already in system"}, 409


@addresses_bp.route("/<int:address_id>", methods=["Delete"])
def delete_address(address_id):
    stmt = db.select(Address).filter_by(id=address_id)
    address = db.session.scalar(stmt)
    if address:
        db.session.delete(address)
        db.session.commit()
        return {"messgage": f"address with id{address_id} deleted"}
    else:
        return {"message": f"address with {address_id} does not exist"}, 404
