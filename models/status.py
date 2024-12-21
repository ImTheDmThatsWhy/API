from init import db, ma
from marshmallow import fields
from marshmallow.validate import Length, And, Regexp
from marshmallow import fields


class Status(db.Model):
    __tablename__ = "statuses"

    id = db.Column(db.Integer, primary_key=True)
    status_name = db.Column(db.String(100), nullable=False)
    thesis = db.relationship("Thesis", back_populates="status")


class StatusSchema(ma.Schema):
    status_name = fields.String(
        required=True,
        validate=And(
            Length(min=3, error="status_name must be at least 3 characters long"),
            Regexp("^[A-Za-z][A-Za-z]*$", error="Only letters, and spaces are allowed"),
        ),
    )
    thesis = fields.List(fields.Nested("ThesisSchema", exclude=["status"]))

    class Meta:
        fields = ("id", "status_name")


status_schema = StatusSchema()
statuses_schema = StatusSchema(many=True)
