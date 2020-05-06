# web_app/routes/home_routes.py

from flask import Blueprint, render_template, redirect, request, flash

home_routes = Blueprint("home_routes", __name__)

@home_routes.route("/")
def index():
    print("VISITED THE HOME PAGE")
    #return "Welcome Home (TODO)"
    return render_template("home.html")