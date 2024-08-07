from db import db
import datetime

class EventModel(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(250), nullable=False)
    series = db.Column(db.String(250), nullable=True)
    series_instance = db.Column(db.Integer, nullable=True)
    # TODO create series DB and convert it to selectfield in the form
    date_from = db.Column(db.Date, nullable=False)
    date_to = db.Column(db.Date, nullable=False)
    country = db.Column(db.String(3), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    surface = db.Column(db.String(250), nullable=False)
    distance = db.Column(db.Float, nullable=True)
    ss_total = db.Column(db.Integer, nullable=False)

    # MtM w/ drivers
    drivers = db.relationship("DriverModel", back_populates="events", secondary="event_driver_link")

    # OtM w/ event_entries
    event_entries = db.relationship("EventEntryModel", back_populates="event")

    @property
    def year(self):
        return self.date_from.year

    @property
    def status(self):
        today = datetime.datetime.now()
        if self.date_from < today.date() < self.date_to:
            return 'live'
        elif self.date_from > today.date():
            return 'upcoming'

