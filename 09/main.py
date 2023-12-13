from flask import Flask, render_template
from flask_marshmallow import Marshmallow
from flask_socketio import SocketIO
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func


app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'cibertec123'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///app.db"

ma = Marshmallow(app)

db = SQLAlchemy(app)

migrate = Migrate(app, db)

socketio = SocketIO(app)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.Text, nullable=False)
    message = db.Column(db.Text, nullable=False)
    # importance # low, high
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Message {self.id}>"


class MessageSchema(ma.Schema):
    class Meta:
        fields = ("id", "user", "message", "created_at")
        model = Message
        datetimeformat = "%Y-%m-%d-%H:%M"


message_schema = MessageSchema()
messages_schema = MessageSchema(many = True)


@app.route("/")
def home():
    messages_data = Message.query.all()
    messages = messages_schema.dump(messages_data)
    return render_template("home.html", messages=messages)
    

def messagesReceived(methods = ["GET", "POST"]):
    print("message was received")


@socketio.on("messages")
def handle_messages(data, methods=["GET", "POST"]):
    message = Message(**data)
    db.session.add(message)
    db.session.commit()
    print("received data: " + str(data))
    socketio.emit("messages-responses", data, callback=messagesReceived)


@socketio.on("welcome")
def handle_welcome(data, methods=["GET", "POST"]):
    print("received json: " + str(data))


if __name__ == '__main__':
    socketio.run(app)