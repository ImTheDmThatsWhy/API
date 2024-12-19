# from marshmallow import fields
from init import db, ma


class Student_supervisor(db.Model):
    __tablename__ = "student_supervisors"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    supervisor_id = db.Column(db.Integer, db.ForeignKey("supervisors.id"), nullable=False)

    # student = db.relationship("student", back_populates= "student_supervisors")
    # supervisor = db.relationship("supervisor", back_populates="student_supervisors")


class Student_supervisorSchema(ma.Schema):
    # student = fields.Nested("StudentSchema", only=["name", "email"])
    # supervisor = fields.Nested ("supervisorSchema", only=["name","phone"])

    # supervisor = fields.Nested("supervisorSchema", only=["supervisors_id"])
    # student = fields.Nested ("StudentSchema", only=["students_id"])
    class Meta:
        fields = ("student_id", "supervisor_id")


student_supervisor_schema = Student_supervisorSchema()
student_supervisors_schema = Student_supervisorSchema(many=True)
