from marshmallow import fields
from init import db, ma


class Professor(db.Model):
    __tablename__ = "Professors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.VARCHAR(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey("faculties.id"), nullable=False)


class ProfessorSchema(ma.Schema):
    ordered = True
    faculty = fields.Nested("FacultySchema", only=["faculty_id"])

    class Meta:
        fields = ["id", "name", "phone", "email", "faculty_id"]


professor_schema = ProfessorSchema()
professors_schema = ProfessorSchema(many=True)
