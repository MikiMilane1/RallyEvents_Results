from db import db


class EventDriverLink(db.Model):
    __tablename__ = "event_driver_link"

    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey("drivers.id"))
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"))
