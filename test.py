import os

from utils.detai import ocr_file

text_ocr = ocr_file("static/demo/65.pdf", False, True, True, False)
if os.path.isfile('text.txt'):
	os.remove('text.txt')
with open('text.txt', 'a+') as file:
	file.write(text_ocr)
# print(text_ocr)
