import flask
from flask import Flask, flash, request, redirect, render_template, url_for
import urllib.request
from werkzeug.utils import secure_filename
import os

app = flask.Flask(__name__)

UPLOAD_FOLDER = '/home/tranmanhdat/project/OCR_web/static/uploads/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config["DEBUG"] = True
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('home.html')
@app.route('/', methods=['POST'])
def upload_file():
	if request.method == 'POST' :
        # check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		if file.filename == '':
			flash('No file selected for uploading')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			flash('File upload success')
			# file_path = 'uploads/' + filename
			text_ocr = ''
			return render_template('index.html', file_name = filename ,text_ocr = text_ocr) 
		else:
			flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
			return redirect(request.url)
if __name__ == "__main__":
    app.run()