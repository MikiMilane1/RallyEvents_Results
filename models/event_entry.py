from sqlalchemy.ext.hybrid import hybrid_property

from db import db
import datetime as dt
from functions import add_time


class EventEntryModel(db.Model):
    __tablename__ = 'event_entries'

    id = db.Column(db.Integer, primary_key=True)
    start_number = db.Column(db.Integer, nullable=True)
    car = db.Column(db.String, nullable=True)

    # MtO w/ event
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), unique=False, nullable=False)
    event = db.relationship("EventModel", back_populates="event_entries")

    # MtO w/ driver
    driver_id = db.Column(db.Integer, db.ForeignKey("drivers.id"), unique=False, nullable=False)
    driver = db.relationship("DriverModel", back_populates="event_entries")

    # OtM w/ ss
    special_sections = db.relationship("SSModel", back_populates="event_entry")

    # MtO w/ team
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"), unique=False, nullable=False)
    team = db.relationship("TeamModel", back_populates="event_entries")

    @property
    def event_name(self):
        return self.event.name

    @property
    def driver_name(self):
        return self.driver.full_name

    @property
    def afters(self):
        afters_list = []
        time_sum = dt.time(
            hour=0,
            minute=0,
            second=0,
            microsecond=0)
        for ss in self.special_sections:
            time_sum = add_time(time_sum, ss.time)
            afters_list.append(time_sum)
        return afters_list

    @property
    def afters_str(self):
        afters_list_str = [str(item)[3:-2] for item in self.afters]
        return afters_list_str

    @hybrid_property
    def finish_time(self):
        time_sum = dt.time(
            hour=0,
            minute=0,
            second=0,
            microsecond=0)
        for ss in self.special_sections:
            time_sum = add_time(time_sum, ss.time)
        return time_sum
