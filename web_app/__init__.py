# web_app/__init__.py

import os
from dotenv import load_dotenv
from flask import Flask

from web_app.routes.home_routes import home_routes
from web_app.routes.movie_routes import movie_routes

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", default="super secret")

def page_not_found(e):
    return jsonify(error=str(e)), 404

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = SECRET_KEY

    app.register_error_handler(404, page_not_found)

    app.register_blueprint(home_routes)
    app.register_blueprint(movie_routes)

    return app

if __name__ == "__main__":
    my_app = create_app()
    my_app.run(debug=True)