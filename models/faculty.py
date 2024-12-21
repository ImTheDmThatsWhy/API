from init import db, ma
from marshmallow.validate import Length, And, Regexp
from marshmallow import fields


class Faculty(db.Model):
    __tablename__ = "faculties"

    id = db.Column(db.Integer, primary_key=True)
    faculty_name = db.Column(db.String(300), nullable=False)


class FacultySchema(ma.Schema):
    faculty_name = fields.String(
        required=True,
        validate=And(
            Length(min=3, error="faculty_name must be at least 3 characters long"),
            Regexp("^[A-Za-z][A-Za-z]*$", error="Only letters, and spaces are allowed"),
        ),
    )
    faculty_id = fields.String(
        required=True,
        validate=And(
            Length(min=1, error="number cannot be empty"),
            Regexp("^[0-9]+$", error="Only numbers"),
        ),
    )

    class Meta:
        fields = ("id", "faculty_name")


faculty_schema = FacultySchema()
faculties_schema = FacultySchema(many=True)
