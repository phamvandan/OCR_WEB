import flask
from flask import Flask, flash, request, redirect, render_template, url_for
import urllib.request
from werkzeug.utils import secure_filename
import os
from utils.supportFunc import preprocessFile
import requests

app = flask.Flask(__name__)

UPLOAD_FOLDER = '/home/trandat/project/OCR_WEB/static/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
currentId = ''
currentFile = ''
current_folderPath = ''
app.config["DEBUG"] = True
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
	file_upload = []
	for line in open("uploadedFile.txt","r+"):
		file_upload.append(line)
	return render_template('home.html', file_upload=file_upload)
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
			f = open("currentID.txt","r")
			global currentId, current_folderPath, currentFile
			currentId = f.readline()
			f.close()
			f = open("currentID.txt","w")
			f.writelines(str(int(currentId)+1))
			f.close()
			folder_files = os.path.join(app.config['UPLOAD_FOLDER'], str(currentId))
			if not os.path.exists(folder_files):
				try:
					original_umask = os.umask(0)
					os.makedirs(folder_files, mode=0x777, exist_ok=False)
				finally:
					os.umask(original_umask)
			filename = currentId+"/"+secure_filename(file.filename)
			currentFile = secure_filename(file.filename)
			file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
			current_folderPath = folder_files
			# print("Current ID "+str(currentId))
			# print("current folderPath "+current_folderPath)
			file.save(file_path)
			flash('File upload success')
			text_ocr = preprocessFile("pdf", folder_files+"/", file.filename+".txt" )
			text_edit = text_ocr
			return render_template('index.html', file_name = filename ,text_ocr = text_ocr, text_edit=text_edit) 
		else:
			flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
			return redirect(request.url)
@app.route('/saveFile/', methods =['POST'])
def saveFile():
	global currentFile, currentId, current_folderPath
	text = request.form['text_edit']
	# print(current_folderPath+"aa")
	# print("current ID "+currentId)
	f = open(os.path.join(current_folderPath,"corrected.txt"),"w+")
	f.write(text)
	f.close()
	with open("uploadedFile.txt","a") as fin:
		fin.writelines(currentFile+"\n")
	with open(os.path.join(current_folderPath,"upLoadName.txt"),"w+") as fin:
		fin.writelines(request.form['uploadPersonName'])
	return redirect(url_for('home'))
if __name__ == "__main__":
    app.run()