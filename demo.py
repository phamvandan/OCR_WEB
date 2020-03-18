import os
import re

import flask
import requests
from flask import flash, request, redirect, render_template, send_from_directory
from werkzeug.utils import secure_filename

from support import listToString, add_tag
from utils.detai import ocr_file

app = flask.Flask(__name__)

app.secret_key = "eDocument"
app.config["DEBUG"] = True
app.config['UPLOAD_FOLDER'] = os.getcwd() + '/static/demo'
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['PDF', 'pdf', 'png', 'jpg', 'jpeg', 'PNG', 'JPG', 'JPEG'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
            filepath = os.path.join(str(app.config['UPLOAD_FOLDER']), filename)
            file.save(filepath)
            global currentFile
            currentFile = filename
            name = os.path.splitext(filepath)[0]
            if os.path.exists(name + '.docx'):
                os.remove(name + '.docx')
            text = ocr_file(filepath, True, True, True, False)
            text_ocr = text
            global url
            text = re.sub('"', '', text).strip()
            text = re.sub('\'', '', text).strip()
            text = re.sub(r'\\', '', text).strip()
            text = re.sub(r'\n', ' ', text).strip()
            text = re.sub(r'\r', ' ', text).strip()
            text = re.sub(r'\t', ' ', text).strip()
            text = re.sub('$', '', text).strip()
            payload = "{\n\t\"id\":\"" + filename + "\",\n\t\"content\":\"" + text + "\"\n}"
            headers = {
                'content-type': "application/json",
                'cache-control': "no-cache",
                'postman-token': "ff99f43e-4466-f28d-62dd-2a485be5ea3f"
            }
            response = requests.request("POST", url, data=payload.encode('utf-8'), headers=headers)
            return render_template('showFile.html', file_name=filename, text_ocr=text_ocr, pdf=pdf_type(filename))


@app.route('/upload_files', methods=['POST'])
def upload_files():
    if request.method == 'POST':
        files = request.files.getlist('file')
        if files.count == 0:
            flash('No file selected for uploading')
            return redirect(request.url)
        else:
            filenames = []
            texts = []
            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    filepath = os.path.join(str(app.config['UPLOAD_FOLDER']), filename)
                    file.save(filepath)
                    filenames.append(filename)
                    global currentFile
                    currentFile = filename
                    name = os.path.splitext(filepath)[0]
                    if os.path.exists(name + '.docx'):
                        os.remove(name + '.docx')
                    text = ocr_file(filepath, True, True, True, False)
                    text_ocr = text
                    global url
                    text = re.sub('"', '', text).strip()
                    text = re.sub('\'', '', text).strip()
                    text = re.sub(r'\\', '', text).strip()
                    # text = re.sub('\\','',text).strip()
                    text = re.sub(r'\n', ' ', text).strip()
                    text = re.sub(r'\r', ' ', text).strip()
                    text = re.sub(r'\t', ' ', text).strip()
                    text = re.sub('$', '', text).strip()
                    payload = "{\n\t\"id\":\"" + filename + "\",\n\t\"content\":\"" + text + "\"\n}"
                    headers = {
                        'content-type': "application/json",
                        'cache-control': "no-cache",
                        'postman-token': "ff99f43e-4466-f28d-62dd-2a485be5ea3f"
                    }
                    response = requests.request("POST", url, data=payload.encode('utf-8'), headers=headers)
                    texts.append(text_ocr)
            return render_template('showFiles.html', file_names=filenames, text_ocr=texts, count=len(filenames),
                                   pdf=pdf_types(filenames))


@app.route('/download_file/<filename>')
def download_file(filename):
    # print(filename)
    # global currentFile
    # #print("download "+str(currentFile))
    return send_from_directory(directory=app.config['UPLOAD_FOLDER'], filename=os.path.splitext(filename)[0] + '.docx',
                               as_attachment=True)


@app.route('/download_file_origin/<filename>')
def download_file_origin(filename):
    # print(filename)
    return send_from_directory(directory=app.config['UPLOAD_FOLDER'], filename=filename, as_attachment=True)


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
              "\n\t\t\t\t\"query\":\"" + text + "\",\n\t\t\t\t\"fuzziness\":5\n\t\t\t}\n\t\t}\n\t}\n} "
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
    sources = jsondata['hits']['hits']
    filenames = []
    contents = []
    for i, source in enumerate(sources):
        file = source['_source']
        filenames.append(file['id'])
        content = add_tag(words, file['content'])
        content = content.split(".")
        rs = []
        for t in content:
            if "<b>" in t:
                rs.append(t)
        content = listToString(rs)
        contents.append(content)
    search_result = {}
    for i in range(0, len(filenames)):
        search_result[filenames[i]] = contents[i]
    return render_template('resultSearch.html', filenames=filenames, contents=contents, count=len(filenames))


@app.route('/view_origin/<filename>')
def view_origin(filename):
    filepath = os.path.join(str(app.config['UPLOAD_FOLDER']), filename)
    txt_path = str(os.path.splitext(filepath)[0]) + '.txt'
    with open(txt_path, 'r+') as f:
        text = f.read()
    return render_template('view_origin.html', file_name=filename, text_ocr=text, pdf=pdf_type(filename))


def init():
    if not os.path.exists(str(app.config['UPLOAD_FOLDER'])):
        os.makedirs(str(app.config['UPLOAD_FOLDER']))


def pdf_type(filename):
    return os.path.splitext(filename)[-1].lower() == '.pdf'


def pdf_types(filenames):
    pdf = []
    for i in range(0, len(filenames)):
        pdf.append(os.path.splitext(filenames[i])[-1].lower() == '.pdf')
    return pdf


if __name__ == "__main__":
    init()
    # app.run(host='10.42.49.111',port=80)
    app.run()
