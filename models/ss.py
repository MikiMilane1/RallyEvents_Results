from db import db


class SSModel(db.Model):
    __tablename__ = "special_sections"

    id = db.Column(db.Integer, primary_key=True)
    ss_num = db.Column(db.Integer, nullable=False)
    time = db.Column(db.Time, nullable=True)
    distance = db.Column(db.Integer, nullable=True)

    # MtO w/ result
    result_id = db.Column(db.Integer, db.ForeignKey("results.id"), unique=False, nullable=False)
    result = db.relationship("ResultModel", back_populates="special_sections")

    @property
    def time_str(self):
        return str(self.time)[3:-3]
