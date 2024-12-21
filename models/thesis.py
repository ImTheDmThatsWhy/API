from marshmallow import fields
from init import db, ma
from marshmallow.validate import Length, And, Regexp


class Thesis(db.Model):
    __tablename__ = "theses"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    student_id = db.Column(
        db.Integer, db.ForeignKey("students.id"), nullable=False, unique=True
    )
    status_id = db.Column(db.Integer, db.ForeignKey("statuses.id"), nullable=False)
    status = db.relationship("Status", back_populates="thesis")


class ThesisSchema(ma.Schema):
    name = fields.String(
        required=True,
        validate=And(
            Length(min=10, error="Name must be at least 10 characters long"),
            Regexp("^[A-Za-z][A-Za-z]*$", error="Only letters, and spaces are allowed"),
        ),
    )
    status_id = fields.String(
        required=True,
        validate=And(
            Length(min=1, error="number cannot be empty"),
            Regexp("^[0-9]+$", error="Only numbers"),
        ),
    )

    ordered = True
    status = fields.Nested("StatusSchema", only=["status_name"])

    class Meta:
        fields = ("id", "name", "student_id", "status", "status_id")


Thesis_schema = ThesisSchema()
Theses_schema = ThesisSchema(many=True)
