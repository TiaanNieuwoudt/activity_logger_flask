from db import db
import datetime


class ActivityModel(db.Model):
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    start_time = db.Column(db.String)
    end_time = db.Column(db.String)

    date = db.Column(db.String(80), default=datetime.date.today())
    calendar = db.relationship('CalendarModel')

    def __init__(self, name, start_time, end_time, date):
        self.name = name
        self.start_time = start_time
        self.end_time = end_time
        self.date = date

    def json(self):
        return {'name': self.name, 'start_time': self.start_time, 'end_time': self.end_time, 'date': self.date}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).all()

    @classmethod
    def find_by_date(cls, date):
        return cls.query.filter_by(date=date).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
