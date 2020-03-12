from flask import Flask
from flask_restful import Api
from resources.activity import ActivityList, Activity
from resources.calendar import Calendar, DateList
from resources.time import TimeSpent, TotalTime, ActivityByTime, TopActivity

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(Activity, '/activity/<string:name>')
api.add_resource(ActivityList, '/activities')
api.add_resource(TimeSpent, '/time_spent/<string:name>')
api.add_resource(Calendar, '/get_date/<string:date>')
api.add_resource(DateList, '/all_dates')
api.add_resource(TotalTime, '/total_time_spent/<string:date>')
api.add_resource(ActivityByTime, '/activity_at_time/<string:date>')
api.add_resource(TopActivity, '/combine_activities/<string:date>')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(debug=True)