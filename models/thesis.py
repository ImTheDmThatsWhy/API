from init import db, ma


class Thesis(db.Model):
    __tablename__ = "Theses"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    grade = db.Column(db.String(100), nullable=False, unique=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    professor_id = db.Column(db.String, db.ForeignKey("professors.id"), nullable=False)


class ThesisSchema(ma.Schema):
    class Meta:
        fields = ("id", "description", "grade", "student_id", "professor_id")


Thesis_schema = ThesisSchema()
Theses_schema = ThesisSchema(many=True)
