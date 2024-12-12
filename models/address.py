from init import db, ma
class Address(db.Model):
    __tablename__="addresses"
    id = db.Column(db.Integer, primary_key=True)
    street_number = db.Column (db.Integer, nullable=False)
    street = db.Column(db.String(200), nullable=False)
    suburb =  db.Column(db.String(200), nullable=False)
    postcode = db.Column(db.Integer, nullable=False)
    state = db.Column(db.String(200), nullable=False)

class AddressSchema(ma.Schema):
    class Meta:
        fields=("id", "street_number", "street", "postcode", "state")
address_schema = AddressSchema()
addresses_schema = AddressSchema(many=True)