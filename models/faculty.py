from init import db, ma


class Faculty(db.Model):
    __tablename__ = "faculties"

    id = db.Column(db.Integer, primary_key=True)
    faculty_name = db.Column(db.String(100), nullable=False)


class FacultySchema(ma.Schema):
    class Meta:
        fields = ("id", "faculty_name")


faculty_schema = FacultySchema
faculties_schema = FacultySchema(many=True)
