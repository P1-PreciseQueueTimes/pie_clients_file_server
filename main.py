from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/post/testing",methods=["POST"])
def receive_post():
    request_data = request.get_json()

    name = request_data["name"]

    age = request_data["age"]

    return "Name: {}, Age: {}".format(name,age) 
