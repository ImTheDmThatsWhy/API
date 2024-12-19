from init import db, ma


class Thesis(db.Model):
    __tablename__ = "Theses"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    student_id = db.Column(
        db.Integer, db.ForeignKey("students.id"), nullable=False, unique=True
    )
    status_id = db.Column(db.Integer, db.ForeignKey("statuses.id"), nullable=False)


class ThesisSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "grade", "student_id", "status_id")


Thesis_schema = ThesisSchema()
Theses_schema = ThesisSchema(many=True)
