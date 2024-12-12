from flask import Blueprint, request
from init import db 
from models.address import Address, addresses_schema, address_schema
addresses_bp= Blueprint("addresses",__name__,url_prefix="/addresses")

@addresses_bp.route("/")
def get_addresses():
    stmt = db.select(Address)
    addresses_list = db.session.scalars(stmt)
    data = addresses_schema.dump(addresses_list)
    return data

@addresses_bp.route("/<int:address_id>")
def get_address(address_id):
 stmt=db.select(Address).filter_by(id=address_id)
 address=db.session.scalar(stmt)
 if address:
    data=address_schema.dump(address)
    return data
 else:
    return {"message":f"address with id{address_id} not found"}, 404
 
@addresses_bp.route("/", methods=["POST"])
def create_address():
    body_data=request.get_json()
    new_address=Address(
    street_number=body_data.get("street_number"),
    street=body_data.get("street"),
    suburb=body_data.get("suburb"),
    postcode=body_data.get("postcode"),
    state=body_data.get("state")
    )
    db.session.add(new_address)
    db.session.commit()
    return address_schema.dump(new_address), 201