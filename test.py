# text_ocr = ocr_file("static/demo/1.pdf", False, True, 0, True)
# if os.path.isfile('text.txt'):
# 	os.remove('text.txt')
# with open('text2.txt', 'a+') as file:
# 	file.write(text_ocr)
# print(text_ocr)

# ocr_file_ = OcrFile("static/demo/83.pdf", False, True, 0, True)
# text_ocr = ocr_file_.run()
# with open('text.txt', 'a+') as file:
# 	file.write(text_ocr)

import cv2

img = cv2.imread(
	'/home/trandat/project/eDocument/OCR_WEB/static/demo/72575621_1931909776955048_8231865659613511680_o_1.jpg')
cv2.imshow('aaa', img)
cv2.waitKey()
