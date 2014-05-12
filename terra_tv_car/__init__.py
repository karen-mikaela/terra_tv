from flask import Flask
from flask.ext.mongoengine import MongoEngine

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {'DB': "terra_car"}
app.config["SECRET_KEY"] = "mys3cr3t3k3y"

db = MongoEngine(app)

def register_blueprints(app):
    from terra_tv_car.views import cars
    app.register_blueprint(cars)

register_blueprints(app)

if __name__ == '__main__':
    app.run()

