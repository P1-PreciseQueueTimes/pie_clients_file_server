from flask import Flask, request,render_template
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/post/testing",methods=["POST"])
def receive_post():
    request_data = request.get_json()

    host_name = request_data["host_name"]

    pie_time = request_data["internal_time"]
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print()
    print("Host Name: {}\nPie Time: {}\nInternal Time".format(host_name,pie_time,current_time))

    return "" 


if __name__ == "__main__":
    app.run()
