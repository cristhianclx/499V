from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.sql import func


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///app.db" # "postgresql://postgres:sistemas@127.0.0.1:5432/cibertec"

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return "<User {}>".format(self.id)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", backref="user")

    def __repr__(self):
        return "<Message {}>".format(self.id)
    

@app.route("/")
def index():
    return render_template("index.html")
    
@app.route("/users")
def users():
    users_data = User.query.all()
    return render_template("users.html", users=users_data)

@app.route("/users/add", methods=["GET", "POST"])
def users_add():
    if request.method == "GET":
        return render_template("users-add.html")
    if request.method == "POST":
        user = User(id = request.form["id"], name=request.form["name"], age=request.form["age"], content=request.form.get("content", ""))
        db.session.add(user)
        db.session.commit()
        return render_template("users-add.html", message="Usuario agregado")
        # return redirect(url_for("users"))

@app.route("/users/<id>")
def users_by_id(id):
    user = User.query.get_or_404(id)
    return render_template("users-detail.html", user=user)
