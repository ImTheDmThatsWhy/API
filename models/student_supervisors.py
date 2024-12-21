# from marshmallow import fields
from init import db, ma
from marshmallow import fields
from marshmallow.validate import Length, And, Regexp


class Student_supervisor(db.Model):
    __tablename__ = "student_supervisors"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    supervisor_id = db.Column(
        db.Integer, db.ForeignKey("supervisors.id"), nullable=False
    )

    student = db.relationship("Student", back_populates="student_supervisor")
    supervisor = db.relationship("Supervisor", back_populates="student_supervisor")


class Student_supervisorSchema(ma.Schema):

    supervisor = fields.Nested("SupervisorSchema", only=["name", "phone", "faculty_id"])
    student = fields.Nested("StudentSchema", only=["name", "email"])
    
    # supervisor = fields.Nested("SupervisorSchema", only=["supervisors_id"])
    # student = fields.Nested("StudentSchema", only=["students_id"])
    
    supervisor_id = fields.String(
        required=True,
        validate=And(
            Length(min=1, error="number cannot be empty"),
            Regexp("^[0-9]+$", error="Only numbers"),
        ),
    )
    student_id = fields.String(
        required=True,
        validate=And(
            Length(min=1, error="number cannot be empty"),
            Regexp("^[0-9]+$", error="Only numbers"),
        ),
    )

    class Meta:
        fields = ("student_id", "supervisor_id", "student", "supervisor")


student_supervisor_schema = Student_supervisorSchema()
student_supervisors_schema = Student_supervisorSchema(many=True)
