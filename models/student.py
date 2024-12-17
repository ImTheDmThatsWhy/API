from marshmallow import fields
from init import db, ma


class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.VARCHAR(20), nullable=True)
    address_id = db.Column(db.Integer, db.ForeignKey("addresses.id"), nullable=False)


class StudentSchema(ma.Schema):
    ordered=True
    address = fields.Nested ("AddressSchema", only=["addresses_id"])
    class Meta:
        fields = ("id", "name", "email", "phone", "address_id")


student_schema = StudentSchema()
students_schema = StudentSchema(many=True)
