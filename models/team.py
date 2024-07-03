from db import db
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, ForeignKey, Float, Date, Table, Column, select, Time


class TeamModel(db.Model):
    __tablename__ = "teams"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)

    # OtM w/ event entries
    event_entries = db.relationship("EventEntryModel", back_populates="team")