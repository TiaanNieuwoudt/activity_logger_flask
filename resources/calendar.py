from flask_restful import Resource
from models.calendar import CalendarModel
from models.activity import ActivityModel


class Calendar(Resource):

    def get(self, date):
        event = CalendarModel.find_by_date(date)
        if event:
            return {'date': date,
                    'activities': list(map(lambda x: x.json(), ActivityModel.query.filter_by(date=date).all()))}

        return {"message": "date {} not found".format(date)}

    def post(self, date):
        _date = CalendarModel.find_by_date(date)
        if not _date:
            _date.save_to_db()


class DateList(Resource):

    def get(self):
        return {'DateList': list(map(lambda x: x.json(), CalendarModel.query.all()))}

