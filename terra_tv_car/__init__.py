from flask import Flask
import os
from flask.ext.mongoengine import MongoEngine

SETTINGS_PATH = os.path.abspath(os.path.realpath(__file__))
ROOT_PATH = os.path.abspath(os.path.join(SETTINGS_PATH, "../../"))
UPLOAD_FOLDER = os.path.join(ROOT_PATH, "terra_tv_car/photos/")
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {'DB': "terra_car"}
app.config["SECRET_KEY"] = "mys3cr3t3k3y"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config["USERNAME"] = "admin"
app.config["PASSWORD"] = "admin"

db = MongoEngine(app)

def register_blueprints(app):
    from terra_tv_car.views import cars
    app.register_blueprint(cars)
    from terra_tv_car.views import admin
    app.register_blueprint(admin)
register_blueprints(app)

if __name__ == '__main__':
    app.run()
