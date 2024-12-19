from init import db, ma


class Status(db.Model):
    __tablename__ = "statuses"

    id = db.Column(db.Integer, primary_key=True)
    status_name = db.Column(db.String(100), nullable=False)


class StatusSchema(ma.Schema):
    class Meta:
        fields = ("id", "status_name")


status_schema = StatusSchema()
statuses_schema = StatusSchema(many=True)
