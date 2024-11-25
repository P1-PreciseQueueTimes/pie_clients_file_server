from flask import send_file, Flask
from pathlib import Path
import zipfile

def zip_folder(folder_name,out_name):

	fp_zip = Path(out_name)
	path_to_archive = Path(folder_name)

	with zipfile.ZipFile(fp_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
		for fp in path_to_archive.glob("**/*"):
			zipf.write(fp, arcname=fp.relative_to(path_to_archive))

zip_folder("test","test.zip")


app = Flask(__name__)

app.route("/get/testing")
def hello_world():
	return "Hello World!!!"

@app.route("/get/testing/startup/receiver")
def return_files_tut_startup_receiver():
	try:

		return send_file("startup_receiver.sh",download_name="startup.sh",as_attachment=True)
	except Exception as e:
		return str(e)

@app.route("/get/testing/startup/sender")
def return_files_tut_startup_sender():
	try:
		return send_file("startup_sender.sh",download_name="startup.sh",as_attachment=True)
	except Exception as e:
		return str(e)

@app.route('/get/testing/receiver')
def return_files_tut():
	try:
		zip_folder("pie_clients","pie_clients.zip")
		return send_file("pie_clients.zip",download_name="pie_clients.zip",as_attachment=True)
	except Exception as e:
		return str(e)
