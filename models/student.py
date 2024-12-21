from marshmallow import fields
from init import db, ma
from marshmallow.validate import Length, And, Regexp


class Student(db.Model):
    __tablename__ = "students"
    # __table_args__=(db.UniqueConstraint)("email","phone")

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.VARCHAR(20), nullable=False, unique=True)
    address_id = db.Column(db.Integer, db.ForeignKey("addresses.id"), nullable=False)
    student_supervisor=db.relationship("Student_supervisor", back_populates="student")

class StudentSchema(ma.Schema):
    student_supervisor=fields.List(fields.Nested("Student_supervisorSchema", exclude=["student"]))
    name = fields.String(
        required=True,
        validate=And(
            Length(min=1, error="Name must be at least 1 characters long"),
            Regexp("^[A-Za-z][A-Za-z]*$", error="Only letters, and spaces are allowed"),
        ),
    )
    phone = fields.String(
        required=True,
        validate=And(
            Length(max=20, error="Too long"),
            Length(min=8, error="minimum 8 numbers"),
            Regexp("^[0-9]+$", error="Only numbers"),
        ),
    )
    address_id = fields.String(
        required=True,
        validate=And(
            Length(min=1, error="number cannot be empty"),
            Regexp("^[0-9]+$", error="Only numbers"),
        ),
    )
    email = fields.String(
        required=True,
        validate=Regexp(
            r"^[a-zA-Z0-9_-]+@[a-zA-Z0-9-]+.[a-zA-Z]+$", error="email format incorrect"
        ),
    )

    class Meta:
        fields = ("id", "name", "email", "phone", "address_id", "student_supervisor")


student_schema = StudentSchema()
students_schema = StudentSchema(many=True)
