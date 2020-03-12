from flask_restful import Resource, reqparse
from models.activity import ActivityModel
from functions.time_funtions import ComputeTime, string_time


class TimeSpent(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('date', required=False, help=' filter query by date')

    def post(self, name):
        total_hours_spent = 0
        total_minutes_spent = 0
        activities = []
        raw_activities = ActivityModel.find_by_name(name)
        date = TimeSpent.parser.parse_args()
        for activity in raw_activities:
            if activity.json()['date'] == date['date']:
                activities.append(activity)
        print(activities)
        for activity in activities:
            event = ComputeTime()
            event.compute_time_spent(activity)
            total_hours_spent = total_hours_spent + event.hours_spent
            total_minutes_spent = total_minutes_spent + event.minutes_spent
        return {"hours spent": total_hours_spent, "minutes spent": total_minutes_spent}


class TotalTime(Resource):

    def get(self, date):
        total_hours = 0
        total_minutes = 0
        data = ActivityModel.find_by_date(date)
        for activity in data:
            time_per_activity = TimeSpent().time_spent(activity)
            hours = time_per_activity[0]
            minutes = time_per_activity[1]

            total_hours = total_hours + hours
            total_minutes = total_minutes + minutes
            if total_minutes >= 60:
                minutes_as_hours = total_minutes // 60
                total_hours = total_hours + minutes_as_hours
                total_minutes = total_minutes % 60

        return {'total hours': total_hours, 'total minutes': total_minutes}


class KnownActivity:
    def __init__(self, hours, minutes):
        self.activity_name = ""
        self.total_hours = hours
        self.total_minutes = minutes


def combine_activities(date):
    known_activities = []
    activities = ActivityModel.find_by_date(date)
    if activities:
        for activity in activities:
            activity_time_spent = ComputeTime().compute_time_spent(activity)
            activity = activity.json()
            hours = activity_time_spent[0]
            minutes = activity_time_spent[1]

            if len(known_activities) > 0:
                for known_activity in known_activities:
                    if activity['name'] == known_activity.activity_name:
                        known_activity.total_hours += hours
                        known_activity.total_minutes += minutes

            else:
                new_activity = KnownActivity(int(hours), int(minutes))
                new_activity.activity_name = activity['name']
                known_activities.append(new_activity)
        return {'combined_activities': list(map(lambda x: (x.activity_name, x.total_hours, x.total_minutes), known_activities))}


class TopActivity(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('date', required=False)

    def get(self, date):
        return combine_activities(date)


class ActivityByTime(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('time', required=False)

    def __init__(self):
        self.time = ActivityByTime.parser.parse_args()['time']

    def find_by_time(self, activity):

        start_time = string_time(activity.start_time)
        end_time = string_time(activity.end_time)
        check_time = string_time(self.time)

        if start_time < end_time:
            if start_time <= check_time <= end_time:
                return activity.json()
        else:
            if check_time >= start_time or check_time <= end_time:
                return activity.json()

    def post(self, date):
        activities = ActivityModel.find_by_date(date)
        if activities:
            for activity in activities:
                return ActivityByTime().find_by_time(activity)








