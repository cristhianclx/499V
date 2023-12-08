from flask import Flask, render_template, request, redirect, url_for
from flask_migrate import Migrate
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///app.db"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

api = Api(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return "<User {}>".format(self.id)


class WorkingResource(Resource):
    def get(self):
        return {
            "working": True,
        }


class UsersResource(Resource):
    def get(self):
        users_data = User.query.all()
        users_results = []
        for user_data in users_data:
            users_results.append({
                "id": user_data.id,
                "name": user_data.name,
                "age": user_data.age,
                "created": user_data.created_at.strftime("%Y-%m-%d-%H:%M"),
            })
        return users_results
    
    def post(self):
        data_user = request.get_json()
        user = User(**data_user)
        db.session.add(user)
        db.session.commit()
        return {
            "id": user.id,
            "name": user.name,
            "age": user.age,
            "created": user.created_at.strftime("%Y-%m-%d-%H:%M"),
        }, 201
    

class UsersByIDResource(Resource):
    def get(self, user_id):
        # TO DO
        return {}


api.add_resource(WorkingResource, "/")
api.add_resource(UsersResource, "/users")
api.add_resource(UsersByIDResource, "/users/<int:user_id>")


@app.route("/users/<id>")
def users_by_id(id):
    user = User.query.get_or_404(id)
    return render_template("users-detail.html", user=user)

@app.route("/users/edit/<id>", methods=["GET", "POST"])
def users_edit_by_id(id):
    user = User.query.get_or_404(id)
    if request.method == "GET":
        return render_template("users-edit.html", user=user)
    if request.method == "POST":
        user.name = request.form["name"]
        user.age = request.form["age"]
        user.content = request.form.get("content", "")
        db.session.add(user)
        db.session.commit()
        return render_template("users-edit.html", user=user, message="Usuario actualizado")

@app.route("/users-delete/<id>", methods=["GET", "POST"])
def users_delete_by_id(id):
    user = User.query.get_or_404(id)
    if request.method == "GET":
        return render_template("users-delete.html", user=user)
    if request.method == "POST":
        user = User.query.filter_by(id = id).first()
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for("users"))

@app.route("/messages-by-user/<user_id>")
def messages_by_user(user_id):
    user = User.query.filter_by(id = user_id).first()
    messages = Message.query.filter_by(user = user).all()
    return render_template("messages-by-user.html", user=user, messages=messages)

@app.route("/messages-add/<user_id>", methods=["GET", "POST"])
def messages_add(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == "GET":
        return render_template("messages-add.html", user=user)
    if request.method == "POST":
        message = Message(id = request.form["id"], content=request.form["content"], user=user)
        db.session.add(message)
        db.session.commit()
        return render_template("messages-add.html", user=user, message="Mensaje agregado")

