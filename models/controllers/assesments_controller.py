from flask import Blueprint, request
from init import db 
from models.address import Address, address_schema, addresses_schema
addresses_bp = Blueprint ("addresses", __name__, url_prefix="/addresses")  

@addresses_bp.route("/")
def get_addresses():
    stmt = db.select(Address)
    addresses_list = db.session.scalars(stmt)
    data = addresses_schema.dump(addresses_list)
    return data

