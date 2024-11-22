from flask import send_file, Flask


app = Flask(__name__)


@app.route('/get/testing/receiver')
def return_files_tut():
	try:
		return send_file("pie_clients.zip",download_name="pie_clients.zip",as_attachment=True)
	except Exception as e:
		return str(e)
