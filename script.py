import os
import re

import requests

from utils.ocr import OcrFile

files = os.listdir('corrected/')
mac = 'user_1'
document = 'document'
ip = "http://localhost:9200"
url = ip + "/" + mac + "/" + document + "/"

for file in files:
	filename = file.split(".")[0] + '.pdf'
	# path_dir = '/media/trandat/Documents/AnhVietAnh/testdata/SoVanBanDi'
	path_dir = 'static/demo'
	path_to_file = os.path.join(path_dir, filename)
	# shutil.copyfile(path_to_file, '/home/trandat/project/eDocument/OCR_WEB/static/demo/'+filename)
	print(path_to_file)
	# print(url)
	ocr = OcrFile(path_to_file, True, 0, True, True, True)
	text = ocr.run()
	text_ocr = text
	text = text.lower()
	text = re.sub('"', '', text).strip()
	text = re.sub('\'', '', text).strip()
	text = re.sub(r'\\', '', text).strip()
	text = re.sub(r'\n', ' ', text).strip()
	text = re.sub(r'\r', ' ', text).strip()
	text = re.sub(r'\t', ' ', text).strip()
	text = re.sub('$', '', text).strip()
	payload = "{\n\t\"content\":\"" + text + "\"\n}"
	headers = {
		'content-type': "application/json",
		'cache-control': "no-cache",
		'postman-token': "ff99f43e-4466-f28d-62dd-2a485be5ea3f"
	}
	response = requests.request("POST", url + filename,
	                            data=payload.encode('utf-8'),
	                            headers=headers)
