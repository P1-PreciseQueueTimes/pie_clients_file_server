from flask import send_file, Flask


app = Flask(__name__)

@app.route("/get/testing/startup")

def return_files_tut_startup():
	try:
		return send_file("startup.sh",download_name="startup.sh",as_attachment=True)
	except Exception as e:
		return str(e)

@app.route('/get/testing/receiver')
def return_files_tut():
	try:
		return send_file("pie_clients.zip",download_name="pie_clients.zip",as_attachment=True)
	except Exception as e:
		return str(e)
