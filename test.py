from utils.ocr import OcrFile

# text_ocr = ocr_file("static/demo/1.pdf", False, True, 0, True)
# if os.path.isfile('text.txt'):
# 	os.remove('text.txt')
# with open('text2.txt', 'a+') as file:
# 	file.write(text_ocr)
# print(text_ocr)

ocr_file_ = OcrFile("static/demo/1.pdf", False, True, 0, True)
text_ocr = ocr_file_.run()
with open('text.txt', 'a+') as file:
	file.write(text_ocr)
