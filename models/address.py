from init import db, ma
from marshmallow.validate import Length, And, Regexp
from marshmallow import fields


class Address(db.Model):
    __tablename__ = "addresses"
    id = db.Column(db.Integer, primary_key=True)
    street_number = db.Column(db.Integer, nullable=False)
    street = db.Column(db.String(200), nullable=False)
    suburb = db.Column(db.String(200), nullable=False)
    postcode = db.Column(db.Integer, nullable=False)
    state = db.Column(db.String(200), nullable=False)


class AddressSchema(ma.Schema):
    street = fields.String(
        required=True,
        validate=And(
            Length(min=2, error="street must be at least 2 characters long"),
            Regexp("^[A-Za-z][A-Za-z]*$", error="Only letters, and spaces are allowed"),
        ),
    )
    suburb = fields.String(
        required=True,
        validate=And(
            Length(min=2, error="suburb must be at least 2 characters long"),
            Regexp("^[A-Za-z][A-Za-z]*$", error="Only letters, and spaces are allowed"),
        ),
    )
    state = fields.String(
        required=True,
        validate=And(
            Length(min=2, error="Name must be at least 2 characters long"),
            Regexp("^[A-Za-z][A-Za-z]*$", error="Only letters, and spaces are allowed"),
        ),
    )
    street_number = fields.String(
        required=True,
        validate=And(
            Length(min=1, error="number cannot be empty"),
            Regexp("^[0-9]+$", error="Only numbers"),
        ),
    )

    # postcode = fields.Integer(required=True, validate=And(
    #     Length(min=4, error="postcode must be at least 4 numbers long"),
    #     Regexp('^[0-9]*$', error="Only numbers are allowed")
    # ))
    class Meta:
        fields = ("id", "street_number", "street", "postcode", "state")


address_schema = AddressSchema()
addresses_schema = AddressSchema(many=True)
