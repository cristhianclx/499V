from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String, Column

class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

db.init_app(app)


class User(db.Model):
    
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    last_name = Column(String(50))
    age = Column(Integer)
    language = Column(String(50))
    city = Column(String(50))

    def __init__(self, name=None, last_name=None, age=None, language=None):
        self.name = name
        self.last_name = last_name
        self.age = age
        self.language = language

    def __repr__(self):
        return "<User {}>".format(self.name)


class Message(db.Model):

    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    content = Column(String(150))

    def __repr__(self):
        return "<Message {}>".format(self.id)
    

@app.route("/")
def index():
    return ""


with app.app_context():
    db.create_all()