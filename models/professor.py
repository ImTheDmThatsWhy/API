from marshmallow import fields
from init import db, ma


class Professor(db.Model):
    __tablename__ = "Professors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    phone = db.Column(db.Integer, nullable=True)
    faculty_id = db.Column(db.String, db.ForeignKey("faculties.id"), nullable=False)


class ProfessorSchema(ma.Schema):
    ordered=True
    faculty=fields.Nested("FacultySchema", only=["faculty_id"])
    class Meta:
        fields = ["id", "name", "department", "address"]


professor_schema = ProfessorSchema()
professors_schema = ProfessorSchema(many=True)
