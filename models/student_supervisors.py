from init import db, ma


class Student_supervisor(db.Model):
    __tablename__ = "student_supervisors"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    professor_id = db.Column(db.Integer, db.ForeignKey("professors.id"), nullable=False)


class Student_supervisorSchema(ma.Schema):
    class Meta:
        fields = ("id", "faculty_name")


student_supervisor_schema = Student_supervisorSchema
student_supervisors_schema_schema = Student_supervisorSchema(many=True)
