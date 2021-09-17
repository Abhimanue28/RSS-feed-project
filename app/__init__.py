from flask import Flask

from app.rss.routes import rss


# Creating our flask app
def create_app():

    app = Flask(__name__, template_folder='template')
    # registering all the blueprints
    app.register_blueprint(rss)
    return app
