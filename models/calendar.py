from db import db


class CalendarModel(db.Model):
    __tablename__ = 'calendar'

    date = db.Column(db.String(80), db.ForeignKey('activities.date'), primary_key=True)
    activities = db.relationship('ActivityModel')

    def __init__(self, date):
        self.date = date

    def json(self):
        return {'date': self.date}

    @classmethod
    def find_by_date(cls, date):
        return cls.query.filter_by(date=date).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
