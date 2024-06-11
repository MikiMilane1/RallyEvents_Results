from db import db


class ResultModel(db.Model):
    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key=True)

    # MtO w/ event
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), unique=False, nullable=False)
    event = db.relationship("EventModel", back_populates="results")

    # MtO w/ driver
    driver_id = db.Column(db.Integer, db.ForeignKey("drivers.id"), unique=False, nullable=False)
    driver = db.relationship("DriverModel", back_populates="results")

    # OtM w/ ss
    special_sections = db.relationship("SSModel", back_populates="result")

    @property
    def event_name(self):
        return self.event.name

    def driver_name(self):
        return self.driver.full_name

