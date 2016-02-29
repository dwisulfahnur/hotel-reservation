from flask import Blueprint, render_template, request

home_views = Blueprint('home', __name__, template_folder='../templates')

@home_views.route("/")
def home():
    return render_template("helloworld.html")
