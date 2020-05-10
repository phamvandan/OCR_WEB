import requests

mac = 'user_1'
document = 'document'
ip = "http://localhost:9200"
url = ip + "/" + mac + "/" + document + "/"
filename = "x.jpg"
text = "không có việc gì khó"

payload = "{\n\t\"content\":\"" + text + "\"\n}"
headers = {
	'content-type': "application/json",
	'cache-control': "no-cache",
	'postman-token': "f82016cd-6767-fef2-35e8-639268c3b5b0"
}
response = requests.request("POST", url + filename,
							data=payload.encode('utf-8'),
							headers=headers)

