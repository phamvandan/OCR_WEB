import os
import re

import flask
import requests
from flask import flash, request, redirect, render_template, send_from_directory
from werkzeug.utils import secure_filename

from utils.ocr import OcrFile
from utils.support import add_tag

app = flask.Flask(__name__)

app.secret_key = "eDocument"
app.config["DEBUG"] = True
app.config['UPLOAD_FOLDER'] = os.getcwd() + '/static/demo'
app.config['MAX_CONTENT_LENGTH'] = 20000 * 1024 * 1024
ALLOWED_EXTENSIONS = {'PDF', 'pdf', 'png', 'jpg', 'jpeg', 'PNG', 'JPG', 'JPEG'}


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[
		1].lower() in ALLOWED_EXTENSIONS


currentFile = ''
mac = 'user_1'
document = 'document'
ip = "http://localhost:9200"
url = ip + "/" + mac + "/" + document + "/"


@app.route('/')
def home():
	return render_template('demoHome.html')


@app.route('/UploadFile')
def upload():
	return render_template('demoUpload.html')


@app.route('/UploadFiles')
def uploads():
	return render_template('demoUploadFiles.html')


@app.route('/upload_file', methods=['POST'])
def upload_file():
	if request.method == 'POST':
		file = request.files['file']
		if file.filename == '':
			flash('No file selected for uploading')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			path_to_file = os.path.join(str(app.config['UPLOAD_FOLDER']),
			                            filename)
			file.save(path_to_file)
			global currentFile
			currentFile = filename
			name = os.path.splitext(path_to_file)[0]
			if os.path.exists(name + '.docx'):
				os.remove(name + '.docx')
			ocr = OcrFile(path_to_file, True, 0, True, True, True)
			text = ocr.run()
			# text = ocr_file(path_to_file, True, True, 0, True)
			text_ocr = text
			text = text.lower()
			text = text.replace("\n"," ")
			global url

			payload = "{\n\t\"content\":\"" + text + "\"\n}"
			headers = {
				'content-type': "application/json",
				'cache-control': "no-cache",
				'postman-token': "f82016cd-6767-fef2-35e8-639268c3b5b0"
			}
			response = requests.request("POST", url + filename,
			                            data=payload.encode('utf-8'),
			                            headers=headers)
			print("here here here here here here ",filename,text,url)
			print(filename, pdf_type(filename))
			return render_template('showFile.html', file_name=filename,
			                       text_ocr=text_ocr, pdf=pdf_type(filename))


@app.route('/upload_files', methods=['POST'])
def upload_files():
	if request.method == 'POST':
		files = request.files.getlist('file')
		if files.count == 0:
			flash('No file selected for uploading')
			return redirect(request.url)
		else:
			file_names = []
			texts = []
			for file in files:
				if file and allowed_file(file.filename):
					filename = secure_filename(file.filename)
					path_to_file = os.path.join(
							str(app.config['UPLOAD_FOLDER']), filename)
					file.save(path_to_file)
					file_names.append(filename)
					global currentFile
					currentFile = filename
					print(currentFile)
					name = os.path.splitext(path_to_file)[0]
					if os.path.exists(name + '.docx'):
						os.remove(name + '.docx')
					# print(path_to_file)
					ocr = OcrFile(path_to_file, True, 0, True, True, True)
					text = ocr.run()
					# text = ocr_file(path_to_file, True, True, 0, True)
					text_ocr = text
					text = text.lower()
					global url

					payload = "{\n\t\"content\":\"" + text + "\"\n}"
					headers = {
						'content-type': "application/json",
						'cache-control': "no-cache",
						'postman-token': "ff99f43e-4466-f28d-62dd-2a485be5ea3f"
					}
					response = requests.request("POST", url + filename,
					                            data=payload.encode('utf-8'),
					                            headers=headers)
					texts.append(text_ocr)
			return render_template('showFiles.html', file_names=file_names,
			                       text_ocr=texts, count=len(file_names),
			                       pdf=pdf_types(file_names))


@app.route('/download_file/<filename>/<file_type>')
def download_file(filename, file_type):
	# print(filename)
	# global currentFile
	# #print("download "+str(currentFile))
	if file_type == 'docx':
		print('docx')
		return send_from_directory(directory=app.config['UPLOAD_FOLDER'],
		                           filename=os.path.splitext(filename)[
			                                    0] + '.docx',
		                           as_attachment=True)
	elif file_type == 'txt':
		return send_from_directory(directory=app.config['UPLOAD_FOLDER'],
		                           filename=os.path.splitext(filename)[
			                                    0] + '.txt',
		                           as_attachment=True)

@app.route('/download_file_origin/<filename>')
def download_file_origin(filename):
	# print(filename)
	return send_from_directory(directory=app.config['UPLOAD_FOLDER'],
	                           filename=filename, as_attachment=True)


@app.route('/search')
def search():
	return render_template('search.html')


@app.route('/search_file', methods=['POST'])
def search_file():
	text = request.form['text']
	words = text.split(" ")
	global url
	url_search = url + '_search'
	querystring = {"filter_path": "hits.hits"}
	payload = "{\n\t\"from\":0,\n\t\"size\":10,\n\t\"query\":{\n\t\t\"match\":{\n\t\t\t\"content\":{" \
	          "\n\t\t\t\t\"query\":\"" + text.lower() + "\",\n\t\t\t\t\"fuzziness\":1\n\t\t\t\t}\n    \t}\n\t},\n\t\"highlight\" : {\n\t\t\"pre_tags\" : [\"<b>\"],\n\t\t\"post_tags\" : [\"</b>\"],\n        \"fields\" : {\n            \"content\":{}\n        }\n    }\n}"
	headers = {
		'Content-Type': "application/json",
		'User-Agent': "PostmanRuntime/7.19.0",
		'Accept': "*/*",
		'Cache-Control': "no-cache",
		'Postman-Token': "957df7e3-745d-4525-be9b-db3dc88cbee5,6bd96736-35b1-4106-9dcb-c86e9dce5c31",
		'Host': "localhost:9200",
		'Accept-Encoding': "gzip, deflate",
		'Content-Length': "112",
		'Connection': "keep-alive",
		'cache-control': "no-cache"
	}
	response = requests.request("POST", url_search,
	                            data=payload.encode('utf-8'), headers=headers,
	                            params=querystring)
	if response.status_code == 404:
		file_names = None
		contents = None
		count = 0
	elif response.status_code == 200:
		json_data = response.json()
		sources = json_data['hits']['hits']
		file_names = []
		contents = []
		# print(sources)
		for i, source in enumerate(sources):
			print(source['_score'])
			print(source['_id'])
			if source['_score'] > 0:
				file = source['_source']
				file_name = source['_id']
				file_names.append(file_name)
				content =source['highlight']['content']
				contents.append(content)
		search_result = {}
		count = len(file_names)
		for i in range(0, count):
			search_result[file_names[i]] = contents[i]
	return render_template('resultSearch.html', filenames=file_names,
	                       contents=contents, count=count)


@app.route('/view_origin/<filename>')
def view_origin(filename):
	path_to_file = os.path.join(str(app.config['UPLOAD_FOLDER']), filename)
	txt_path = str(os.path.splitext(path_to_file)[0]) + '.txt'
	with open(txt_path, 'r+') as f:
		text = f.read()
	return render_template('view_origin.html', file_name=filename,
	                       text_ocr=text, pdf=pdf_type(filename))


def create_upload_folder():
	if not os.path.exists(str(app.config['UPLOAD_FOLDER'])):
		os.makedirs(str(app.config['UPLOAD_FOLDER']))


def pdf_type(filename):
	# return filename.lower().endswith('.pdf')
	return os.path.splitext(filename)[-1].lower() == '.pdf'


def pdf_types(file_names):
	pdf = []
	for i in range(0, len(file_names)):
		pdf.append(os.path.splitext(file_names[i])[-1].lower() == '.pdf')
	return pdf


if __name__ == "__main__":
	create_upload_folder()
	# app.run(host='10.42.49.111',port=80)
	app.run(debug=app.config['DEBUG'])
