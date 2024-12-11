from init import db, ma
class Degree_level(db.Model):
    __tablename__="degree_levels"

    id = db.Column(db.Integer, primary_key=True)
    faculty_name = db.Column(db.String(100), nullable=False)
class DegreeSchema(ma.Schema):
    class Meta:
        fields=("id", "faculty_name")
degree_schema = DegreeSchema
degrees_schema = DegreeSchema(many=True)