import os
import time
from pathlib import Path

import cv2

from utils.ScanText import get_text, get_text_layout
from utils.pdf_to_images import pdf_to_images
from utils.skew_process.deskew import Deskew
from utils.table_process.DetectTable import DetectTable
from utils.table_process.find_bb import get_table_coordinate
from utils.text_correction.RuleBase import RuleBase


def handle_file(path_to_file, pdf_file_name, pdf, docx=False, skew=False,
                table_mode=0):
	img = cv2.imread(path_to_file)
	print(type(img))
	rule_base = RuleBase()
	# handle skew
	if skew:
		start = time.time()
		d = Deskew(img)
		img, angle = d.run()
		end = time.time()
		print('skew_process take : ' + "{0:.2f}".format(end - start))
	# handle table with not auto fill
	cv2.imwrite("after_skew.jpg",img)
	start = time.time()
	mask = DetectTable(img.copy()).run(table_mode)
	end = time.time()
	print('table handle take ' + "{0:.2f}".format(end - start))
	mask_img = mask
	start = time.time()
	list_result, list_big_box = get_table_coordinate(mask_img)
	end = time.time()
	print('get_table_coordinate take ' + "{0:.2f}".format(end - start))
	# img = cv2.resize(img, (mask_img.shape[1], mask_img.shape[0]))
	start = time.time()
	if not docx:
		result_table = get_text(list_result, list_big_box, img, rule_base)
	else:
		if not pdf:
			file_name_without_extension = os.path.splitext(path_to_file)[0]
			result_table = get_text_layout(
					list_result, list_big_box, img,
					file_name_without_extension + ".docx")
		else:
			file_name_without_extension = os.path.splitext(pdf_file_name)[
				0]
			result_table = get_text_layout(
					list_result, list_big_box, img,
					file_name_without_extension + ".docx")
	end = time.time()
	print('docx take ' + "{0:.2f}".format(end - start))
	return result_table


pdfExtension = [".pdf", ".PDF"]
imageExtension = [".jpg", ".JPG", ".png", ".PNG"]
debug = True


def ocr_file(file_path, docx, skew_mode, table_mode=0, auto_correct=False):
	"""
	a function help ocr file with input is a file and return result in string
	:param file_path: string to file ocr
	:type file_path: str
	:param docx: True if make a docx file
	:type docx: bool
	:param skew_mode: True if using skew_process
	:type skew_mode: bool
	:param table_mode: 0 - without auto fill table, 1 - auto fill table
	:type table_mode: int
	:param auto_correct: 0 - without auto correct text, 1 - auto correct text
	:type auto_correct: int
	:return: str
	"""
	global debug
	path = Path(file_path)
	filename = path.stem
	extension = path.suffix
	current_folder = path.parent
	result = ""
	if extension in pdfExtension:
		names = []
		count = 0
		# print(current_folder)
		count, _ = pdf_to_images(path, current_folder, True)  # convert to image
		for k in range(1, count + 1):
			names.append(str(k) + ".jpg")
		for image in names:
			print('Start OCR' + str(image) + '-------------------------------')
			image_path = os.path.join(str(current_folder), image)
			start = time.time()
			result_table = handle_file(image_path, file_path, True, docx=docx,
			                           skew=skew_mode, table_mode=table_mode)
			# k = 0
			end = time.time()
			print('Total time OCR ' + str(image) +
			      ' : ' + "{0:.2f}".format(end - start))
			for rs in result_table:
				# if k %4 == 0:
				#     result = result + "\n"
				result = result + (str(rs))
			# k = k+ 1
			if not debug:
				os.remove(image_path)
	elif extension in imageExtension:
		result_table = handle_file(file_path, '', False, docx=docx,
		                           skew=skew_mode, table_mode=table_mode)
		for rs in result_table:
			# if k %4 == 0:
			#     result = result + "\n"
			result = result + (str(rs))
	# k = k+ 1
	if auto_correct:
		rule_base = RuleBase()
		# print(result)
		result = rule_base.correct(result)
	# print(result)
	txt_path = str(os.path.splitext(file_path)[0]) + '.txt'
	if os.path.exists(txt_path):
		os.remove(txt_path)
	with open(txt_path, 'w+') as f:
		f.write(result)
	return result
