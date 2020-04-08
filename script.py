import os
import re
import requests

mac = 'tranmanhdat'
document = 'document'
ip = "http://localhost:9200"
url = ip + "/" + mac + "/" + document + "/"

for r, _, f in os.walk('/home/trandat/project/OCR_WEB/static/demo'):
    for file in f:
        if file.__contains__('.txt'):
            with open(os.path.join(str(r), file)) as f:
                text = f.read()
            text = re.sub('"','',text).strip()
            text = re.sub('\'','',text).strip()
            text = re.sub(r'\\', '',text).strip()
            # text = re.sub('\\','',text).strip()
            text = re.sub(r'\n', ' ', text).strip()
            text = re.sub(r'\r', ' ', text).strip()
            text = re.sub(r'\t', ' ', text).strip()
            text = re.sub('$','',text).strip()
            # text = json.dumps(text)
            print(text)
            print(file)
            filename = os.path.splitext(file)[0]+'.pdf'
            print(filename)
            payload = "{\n\t\"content\":\"" + text + "\"\n}"
            headers = {
                'content-type': "application/json",
                'cache-control': "no-cache",
                'postman-token': "ff99f43e-4466-f28d-62dd-2a485be5ea3f"
            }
            response = requests.request("POST", url + filename,
                                        data=payload.encode('utf-8'),
                                        headers=headers)
            print(response)