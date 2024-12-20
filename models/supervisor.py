from marshmallow import fields
from init import db, ma
from marshmallow.validate import Length, And, Regexp


class Supervisor(db.Model):
    __tablename__ = "supervisors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.VARCHAR(20), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    faculty_id = db.Column(db.Integer, db.ForeignKey("faculties.id"), nullable=False)


class SupervisorSchema(ma.Schema):
    name = fields.String(required=True, validate=And(
        Length(min=3, error="Name must be at least 3 characters long"),
        Regexp('^[A-Za-z][A-Za-z]*$', error="Only letters, and spaces are allowed")
    ))
    email = fields.String(required=True, validate=
    Regexp(r"^[a-zA-Z0-9_-]+@[a-zA-Z0-9-]+.[a-zA-Z]+$", error="email format incorrect"))
    ordered = True
    faculty = fields.Nested("FacultySchema", only=["faculty_id"])

    class Meta:
        fields = ["id", "name", "phone", "email", "faculty_id"]


supervisor_schema = SupervisorSchema()
supervisors_schema = SupervisorSchema(many=True)
