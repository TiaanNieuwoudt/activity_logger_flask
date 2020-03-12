from models.activity import ActivityModel
from flask_restful import Resource, reqparse
from models.calendar import CalendarModel


class Activity(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('start_time', type=str, required=True, help="Filed cannot be left blank")
    parser.add_argument('end_time', type=str, required=True, help="Filed cannot be left blank")
    parser.add_argument('date', type=str, required=False, help="Filed cannot be left blank")

    def get(self, name):
        activities = ActivityModel.find_by_name(name)
        if activities:
            return {'activities': list(map(lambda x: x.json(), activities))}
        return {"message": "Activity with name {} does not exist".format(name)}, 404  # Not found

    def post(self, name):
        data = Activity.parser.parse_args()
        activity = ActivityModel(name, **data)
        try:
            activity.save_to_db()

        except:
            return {"message": "An error occured while inserting activity"}, 500

        save_date = activity.json()['date']
        if not CalendarModel.find_by_date(save_date):
            date = CalendarModel(save_date)
            date.save_to_db()

    def delete(self, name):
        activity = ActivityModel.find_by_name(name)
        if activity:
            activity.delete_from_db()

        return{"message": "Item deleted successfully"}

    def put(self, name):
        data = Activity.parser.parse_args()
        activity = ActivityModel.find_by_name(name)

        if activity is None:
            activity = ActivityModel(name, **data)
        else:
            activity.hours_spent = data['hours_spent']

        activity.save_to_db()
        return activity.json()





class ActivityList(Resource):
    def get(self):
        return {"activities": list(map(lambda x: x.json(), ActivityModel.query.all()))}
