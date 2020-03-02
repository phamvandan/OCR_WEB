import flask
from flask import Flask, flash, request, redirect, render_template, url_for, send_file, abort, send_from_directory, jsonify
import urllib.request
from werkzeug.utils import secure_filename
import requests
from pathlib import Path
from utils.detai import ocrFile
import os, re
import json
import os
app = flask.Flask(__name__)


app.secret_key = "tranmanhdat"
app.config["DEBUG"] = True
app.config['UPLOAD_FOLDER'] = os.getcwd() + '/static/demo'
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['PDF', 'pdf', 'png', 'jpg', 'jpeg', 'PNG', 'JPG' , 'JPEG'])
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

currentFile = ''
mac = 'tranmanhdat'
document = 'document'
ip = "http://localhost:9200"
url = ip+"/"+mac+"/"+document+"/"

@app.route('/')
def home():
    return render_template('demoHome.html')
@app.route('/UploadFile')
def upload():
    # #print("aaaa")
    return render_template('demoUpload.html')
@app.route('/UploadFiles')
def uploads():
    return render_template('demoUploadFiles.html')
@app.route('/uploadFile', methods=['POST'])
def uploadFile():
    if request.method == 'POST':
        # check if the post request has the file part
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(str(app.config['UPLOAD_FOLDER']), filename)
            file.save(filepath)
            #print('upload success : '+filename)
            global currentFile
            currentFile = filename
            name = os.path.splitext(filepath)[0]
            if os.path.exists(name+'.docx'):
                os.remove(name+'.docx')
            text = ocrFile(filepath,True,True, True, True, False)
            text_ocr = text
            global url
            #print(url)
            text = re.sub('"','',text).strip()
            text = re.sub('\'','',text).strip()
            text = re.sub(r'\\', '',text).strip()
            # text = re.sub('\\','',text).strip()
            text = re.sub(r'\n', ' ', text).strip()
            text = re.sub(r'\r', ' ', text).strip()
            text = re.sub(r'\t', ' ', text).strip()
            text = re.sub('$','',text).strip()
            # text = json.dumps(text)
            #print(text)
            payload = "{\n\t\"id\":\""+filename+"\",\n\t\"content\":\""+text+"\"\n}"
            headers = {
                'content-type': "application/json",
                'cache-control': "no-cache",
                'postman-token': "ff99f43e-4466-f28d-62dd-2a485be5ea3f"
                }
            response = requests.request("POST", url, data=payload.encode('utf-8'), headers=headers)
            # #print(response.text)
            return render_template('showFile.html', file_name=filename, text_ocr=text_ocr, pdf = PdfType(filename))
@app.route('/uploadFiles', methods=['POST'])
def uploadFiles():
    if request.method == 'POST':
        # check if the post request has the file part
        files = request.files.getlist('file')
        #print(files)
        if files.count == 0:
            flash('No file selected for uploading')
            return redirect(request.url)
        else:
            filenames =[]
            texts = []
            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    filepath = os.path.join(str(app.config['UPLOAD_FOLDER']), filename)
                    file.save(filepath)
                    filenames.append(filename)
                    #print('upload success : '+filename)
                    global currentFile
                    currentFile = filename
                    name = os.path.splitext(filepath)[0]
                    if os.path.exists(name+'.docx'):
                        os.remove(name+'.docx')
                    text = ocrFile(filepath,True,True, True, True, False)
                    text_ocr = text
                    global url
                    #print(url)
                    text = re.sub('"','',text).strip()
                    text = re.sub('\'','',text).strip()
                    text = re.sub(r'\\', '',text).strip()
                    # text = re.sub('\\','',text).strip()
                    text = re.sub(r'\n', ' ', text).strip()
                    text = re.sub(r'\r', ' ', text).strip()
                    text = re.sub(r'\t', ' ', text).strip()
                    text = re.sub('$','',text).strip()
                    # text = json.dumps(text)
                    #print(text)
                    payload = "{\n\t\"id\":\""+filename+"\",\n\t\"content\":\""+text+"\"\n}"
                    headers = {
                        'content-type': "application/json",
                        'cache-control': "no-cache",
                        'postman-token': "ff99f43e-4466-f28d-62dd-2a485be5ea3f"
                        }
                    response = requests.request("POST", url, data=payload.encode('utf-8'), headers=headers)
                    texts.append(text_ocr)
            # text.replace("\n","\n\n")
            # #print(text)
            return render_template('showFiles.html', file_names=filenames, text_ocr=texts, count=len(filenames), pdf=PdfTypes(filenames))
@app.route('/downloadFile/<filename>')
def downloadFile(filename):
    #print(filename)
    # global currentFile
    # #print("download "+str(currentFile))
    return send_from_directory(directory=app.config['UPLOAD_FOLDER'],filename=os.path.splitext(filename)[0]+'.docx',as_attachment=True)
@app.route('/downloadFileOrigin/<filename>')
def downloadFileOrigin(filename):
    #print(filename)
    return send_from_directory(directory=app.config['UPLOAD_FOLDER'],filename=filename,as_attachment=True)
@app.route('/search')
def search():
    return render_template('search.html')
@app.route('/searchfile' , methods=['POST'])
def searchfile():
    #do something
    text = request.form['text']
    #print("text : "+text)
    global url
    url_search = url+'_search'
    querystring = {"filter_path":"hits.hits._source"}
    payload = "{\n\t\"from\":0,\n\t\"size\":10,\n\t\"query\":{\n\t\t\"match\":{\n\t\t\t\"content\":{\n\t\t\t\t\"query\":\""+text+"\",\n\t\t\t\t\"fuzziness\":2\n\t\t\t}\n\t\t}\n\t}\n}"
    #print(payload)
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
    response = requests.request("POST", url_search, data=payload.encode('utf-8'), headers=headers, params=querystring)
    jsondata = response.json()
    # #print(response.json())
    sources = jsondata['hits']['hits']
    #print(len(sources))
    filenames =[]
    contents =[]
    for i,source in enumerate(sources):
        file = source['_source']
        filenames.append(file['id'])
        contents.append(file['content'][100:300])
    #print(filenames)
    #print(contents)
    searchResult = {}
    for i in range(0,len(filenames)):
        searchResult[filenames[i]] = contents[i]
    return render_template('resultSearch.html',filenames = filenames, contents = contents , count = len(filenames))
@app.route('/viewOrigin/<filename>')
def viewOrigin(filename):
    filepath = os.path.join(str(app.config['UPLOAD_FOLDER']), filename) 
    txtPath = str(os.path.splitext(filepath)[0])+'.txt'
    with open(txtPath,'r+') as f:
        text = f.read()
    #print(text)
    return render_template('viewOrigin.html', file_name=filename, text_ocr=text, pdf =PdfType(filename))

def init():
    if not os.path.exists(str(app.config['UPLOAD_FOLDER'])):
        os.makedirs(str(app.config['UPLOAD_FOLDER']))
def PdfType(filename):
    return (os.path.splitext(filename)[-1].lower() == '.pdf')
def PdfTypes(filenames):
    pdf = []
    for i in range(0,len(filenames)):
        pdf.append(os.path.splitext(filenames[i])[-1].lower() == '.pdf')
    return pdf
if __name__ == "__main__":
    # app.run(host='172.16.1.27',port=80)
    init()
    app.run()