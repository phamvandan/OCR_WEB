import flask
from flask import Flask, flash, request, redirect, render_template, url_for
import urllib.request
from werkzeug.utils import secure_filename
import os
from utils.supportFunc import preprocessFile
import requests
from pathlib import Path

app = flask.Flask(__name__)

staticPath = '/home/trandat/project/OCR_WEB/static'
projectPath = '/home/trandat/project/OCR_WEB'
app.config["DEBUG"] = True

currentFile = ''

@app.route('/')
def home():
	dic = {}
	files =[]
	for r, _, f in os.walk(os.path.join(staticPath, "data")):
		for file in f:
			if file.__contains__("pdf"):
				files.append(file)
				with open(os.path.join(staticPath+'/data',os.path.join("state"+Path(os.path.join(r,file)).stem+".txt")),"r+" ) as fin:
					x = fin.readline()
					dic[file] = x
	for file in files:
		print(file+"\n")
	return render_template('home.html', files=files, dic=dic)
@app.route('/saveFile/', methods =['POST'])
def saveFile():
	global currentFile
	text = request.form['text_edit']
	persionName = request.form['uploadPersonName']
	with open(os.path.join(staticPath,'OCR_edited', Path(currentFile).stem+".txt"),"w+") as f:	
		f.write(text)
	with open(os.path.join(staticPath+'/data',os.path.join("state"+Path(currentFile).stem+".txt")),"w+" ) as fin:
		fin.write('Edited')
	with open(os.path.join(projectPath,"historyEdit.txt"),"a+") as fin:
		fin.write(persionName+"\t"+currentFile+"\n")
	return redirect(url_for('home'))
@app.route	('/editFile/<filename>', methods = ['POST', 'GET'])
def editFile(filename):
	global currentFile
	currentFile =filename
	fileName = Path(filename).stem + ".txt"
	with open(os.path.join(staticPath,'OCR_origin', fileName),"r+") as f:
		text_ocr = f.read()
	print(os.path.join(staticPath,'OCR_origin', fileName))
	with open(os.path.join(staticPath,'OCR_edited', fileName),"r+") as f:	
		text_edit = f.read()
	print(os.path.join(staticPath,'OCR_edited', fileName))
	return render_template('index.html', file_name=filename, text_ocr=text_ocr, text_edit=text_edit)
if __name__ == "__main__":
    # app.run(host='172.16.1.27',port=80)
	app.run()