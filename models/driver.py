from db import db
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, ForeignKey, Float, Date, Table, Column, select, Time


class DriverModel(db.Model):
    __tablename__ = "drivers"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    birth_date = db.Column(db.Date, nullable=True)
    country = db.Column(db.String(40), nullable=True)

    # OtM w/ event entries
    event_entries = db.relationship("EventEntryModel", back_populates="driver")

    # MtM w/ events
    events = db.Relationship("EventModel", back_populates="drivers", secondary="event_driver_link")

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    __table_args__ = (
        db.UniqueConstraint('first_name', 'last_name', 'birth_date', name='uix_1'),
    )
