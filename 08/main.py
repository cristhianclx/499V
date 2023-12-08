from flask import Flask, render_template, request, redirect, url_for
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///app.db"

ma = Marshmallow(app)
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


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", backref="user")

    def __repr__(self):
        return "<Message {}>".format(self.id)


class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "age", "created_at")
        model = User
        datetimeformat = "%Y-%m-%d-%H:%M"


user_schema = UserSchema()
users_schema = UserSchema(many = True)


class WorkingResource(Resource):
    def get(self):
        return {
            "working": True,
        }


class UsersResource(Resource):
    def get(self):
        users_data = User.query.all()
        return users_schema.dump(users_data)
    
    def post(self):
        data_user = request.get_json()
        user = User(**data_user)
        db.session.add(user)
        db.session.commit()
        return user_schema.dump(user), 201
    

class UsersByIDResource(Resource):
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return user_schema.dump(user)
    
    def patch(self, user_id):
        user = User.query.get_or_404(user_id)
        data_user = request.get_json()
        user.name = data_user.get("name", user.name)
        user.age = data_user.get("age", user.age)
        db.session.commit()
        return user_schema.dump(user)

    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {}, 204


api.add_resource(WorkingResource, "/")
api.add_resource(UsersResource, "/users")
api.add_resource(UsersByIDResource, "/users/<int:user_id>")