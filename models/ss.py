from db import db


class SSModel(db.Model):
    __tablename__ = "special_sections"

    id = db.Column(db.Integer, primary_key=True)
    ss_num = db.Column(db.Integer, nullable=False)
    time = db.Column(db.Time, nullable=True)
    distance = db.Column(db.Integer, nullable=True)

    # MtO w/ event_entry
    event_entry_id = db.Column(db.Integer, db.ForeignKey("event_entries.id"), unique=False, nullable=False)
    event_entry = db.relationship("EventEntryModel", back_populates="special_sections")

    @property
    def time_str(self):
        return str(self.time)

    @property
    def event(self):
        return self.event_entry.event

    @property
    def driver(self):
        return self.event_entry.driver
