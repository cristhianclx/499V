from flask import Flask, render_template, request, redirect, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import flask_login


app = Flask(__name__)
app.debug = False
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///app.db"
app.secret_key = "cibertec-python"

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(flask_login.UserMixin):
    def __init__(self, username, password):
        self.id = username
        self.password = password


table_users = {
    "cristhian": User("cristhian", "123456"),
    "genaro": User("genaro", "123456"),
}


@login_manager.user_loader
def user_loader(id):
    return table_users.get(id)


@app.get("/login")
def login_get():
    return render_template("login.html")


@app.post("/login")
def login():
    user = table_users.get(request.form["username"])
    if user is None or user.password != request.form["password"]:
        return redirect(url_for("login"))
    flask_login.login_user(user)
    return redirect(url_for("dashboard"))


@app.route("/dashboard")
@flask_login.login_required
def dashboard():
    return render_template(
        "dashboard.html",
        user=flask_login.current_user
    )


@app.route("/logout")
def logout():
    flask_login.logout_user()
    return redirect(url_for("login"))