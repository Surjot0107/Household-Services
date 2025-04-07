from flask import Flask
from backend.models import *

app = None

def init_app():
    household_app = Flask(__name__)
    household_app.debug = True
    household_app.app_context().push()
    household_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///household.sqlite3"
    db.init_app(household_app)
    print("App started")
    return household_app

app = init_app()
from backend.controllers import *

if __name__ == "__main__":
    app.run()