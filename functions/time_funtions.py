import datetime


class ComputeTime:

    def __init__(self):
        self.hours_spent = 0
        self.minutes_spent = 0

    def compute_time_spent(self, activity):

        starting_hour = int(activity.start_time[0:2])
        ending_hour = int(activity.end_time[0:2])

        starting_minute = int(activity.start_time[3:5])
        ending_minute = int(activity.end_time[3:5])

        self.hours_spent = ending_hour - starting_hour
        minutes_spent = ending_minute - starting_minute

        if minutes_spent < 0:
            self.hours_spent -= 1
            self.minutes_spent += 60

        return self.hours_spent, self.minutes_spent


def string_time(time):
    valid_time = datetime.time(hour=int(time[:2]), minute=int(time[3:5]))
    return valid_time

