from flask import Flask
from flask import request

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, CIBERTEC!</p>"

@app.route("/hello")
def hello_students():
    return "<p>Hello, STUDENTS!</p>"

@app.route("/messages")
def messages():
    return [{"name": "cristhian"}, {"name": "genaro"}]

@app.route("/user/<username>")
def user_username(username):
    return "Hello {}".format(username)

@app.route("/post/<int:post_id>")
def get_post_by_post_id(post_id):
    return "Post: {}".format(post_id)


data = [{
    "user": "cristhian",
    "password": 123456,
}, {
    "user": "genaro",
    "password": 12345678,
}]


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data_input = request.get_json()
        user = data_input.get("user")
        password = data_input.get("password")
        if user and password:
            for i in data:
                if i.get("user") == user and str(i.get("password")) == password:
                    return "valid login"
            return "invalid login"
        else: 
            return "missing parameters"
    else:
        return "you need to login"