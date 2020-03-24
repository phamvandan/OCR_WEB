import os

import cv2
import imutils
import numpy as np
import pytesseract
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT

from utils.table_process.find_bb import IOU


def check_iou_with_above_row(cell1, cell2):
	(x, y, w, h) = cell1
	(x1, y1, w1, h1) = cell2
	if (y1 <= y <= y1 + h1 - 5) or (y <= y1 <= y + h - 5):
		return True
	return False


def check_iou_with_above_cell(cell1, cell2):
	(x, y, w, h) = cell1
	(x1, y1, w1, h1) = cell2
	if (x <= x1 <= x + w) or (x1 <= x <= x1 + w1):
		return True
	return False


def get_string_from_image(box, image, rule_base, auto_correct=True):
	(x, y, w, h) = box
	crop = image[y:y + h, x:x + w]
	string = pytesseract.image_to_string(crop, lang='vie')
	if auto_correct:
		string = rule_base.correct(string)
	cv2.rectangle(image, (x, y), (x + w, y + h), 255, 1)
	return string


def layout_document(image, document, rule_base, auto_correct=True):
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	_, thresh = cv2.threshold(gray, 0, 255,
	                          cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
	# assign a rectangle kernel size
	kernel = np.ones((5, 5), 'uint8')
	par_img = cv2.dilate(thresh, kernel, iterations=5)
	cv2.circle(image, (image.shape[1] // 3, 10), 4, (0, 0, 255), 2)
	# printImage(image)
	# printImage(par_img)
	if imutils.is_cv2() or imutils.is_cv4():
		(conts, hierarchy) = cv2.findContours(par_img.copy(), cv2.RETR_EXTERNAL,
		                                      cv2.CHAIN_APPROX_SIMPLE)
	elif imutils.is_cv3():
		(_, conts, hierarchy) = cv2.findContours(par_img.copy(),
		                                         cv2.RETR_EXTERNAL,
		                                         cv2.CHAIN_APPROX_SIMPLE)
	list_result = []
	if len(conts) > 0:
		conts = imutils.contours.sort_contours(conts)[0]
		for i in range(len(conts)):
			(x, y, w, h) = cv2.boundingRect(conts[i])
			if w < 25 or h < 25 or abs(
					image.shape[1] - w - x) <= 10 or x <= 5 or (
					w < 50 and h < 50):
				# print("over")
				continue
			skip = False
			for index, temp in enumerate(list_result):
				for index1, box in enumerate(temp):
					if IOU(box, (x, y, w, h)):
						## if new box is bigger
						if w * h > box[2] * box[3]:
							list_result[index][index1] = (x, y, w, h)
						skip = True
						break
			if not skip:
				over = False
				for index, temp in enumerate(list_result):
					(x1, y1, w1, h1) = temp[0]
					if abs(y1 - y) <= 5 or (check_iou_with_above_row(temp[0], (
							x, y, w, h)) and x >= (temp[len(temp) - 1][0] +
					                               temp[len(temp) - 1][2])):
						list_result[index].append((x, y, w, h))
						over = True
				if not over:
					list_result.append([(x, y, w, h)])
	## sort
	for index, _ in enumerate(list_result):
		list_result[index] = sorted(list_result[index], key=lambda x: x[0])
	list_result = sorted(list_result, key=lambda x: x[0][1])
	for index, temp in enumerate(list_result):
		for (x, y, w, h) in temp:
			cv2.rectangle(image, (x, y), (x + w, y + h), 255, 1)
	# printImage(image)
	# index = 0
	# while index < len(list_result):
	#     temp = list_result[index]
	#     if index>0:
	#         for index2,boxbelow in enumerate(temp):
	#             (x,y,w,h) = boxbelow
	#             for index1,box in enumerate(list_result[index-1]):
	#                 (x1,y1,w1,h1) = box
	#                 dis = y - (y1+h1)
	#                 if dis >=0 and dis<=3 and check_iou_with_above_cell(box,boxbelow): ## concat box
	#                     list_result[index-1][index1] = (min(x,x1),y1,max(w1,w),h1+h+dis)
	#                     list_result[index].pop(index2)
	#                     if len(list_result[index])==0:
	#                         list_result.pop(index)
	#                         index = index - 1
	#                     print("concat box success")
	#                     # break
	#     index = index + 1
	for k, temp in enumerate(list_result):
		align = WD_TABLE_ALIGNMENT.CENTER
		if len(temp) == 1:
			(x, y, w, h) = temp[0]
			if (x < image.shape[1] / 5 or (
					w > image.shape[1] / 2 and x < image.shape[
				1] / 3)) and k != 1:  ## kiem tra align
				align = WD_TABLE_ALIGNMENT.LEFT
			# print("left")
			elif x > image.shape[1] / 2:
				list_result[k].insert(0, (0, 0, 0, 0))

		table = document.add_table(rows=1, cols=len(temp))
		row_cells = table.rows[0].cells
		for index, (x, y, w, h) in enumerate(temp):
			if (x, y, w, h) == (0, 0, 0, 0):
				string = ""
				p = row_cells[index].add_paragraph(string)
				p.alignment = align
				continue
			string = get_string_from_image((x, y, w, h), image, rule_base,
			                               auto_correct)
			p = row_cells[index].add_paragraph(string)
			p.alignment = align
	return list_result, document


def get_text_layout(list_result, list_big_box, img, doc_name, rule_base,
                    auto_correct=True):
	## open or create docx file
	if not os.path.exists(doc_name):
		dc = Document()
		dc.save(doc_name)
	document = Document(doc_name)

	result = []
	(height, _) = img.shape[:2]
	if len(list_big_box) == 0:
		layout_document(img, document)
		document.save(doc_name)
		string = pytesseract.image_to_string(img, lang='vie')
		if auto_correct:
			string = rule_base.correct(string)
		result.append(string + "\n")
		return result
	big_box_temp = []
	list_y_coord = [0]
	for (_, y, _, h) in list_big_box:
		big_box_temp.append((y, y + h))
		list_y_coord.append(y)
		list_y_coord.append(y + h)
	list_y_coord.append(height)
	for index, y1 in enumerate(list_y_coord):
		if index == len(list_y_coord) - 1:
			break
		y2 = list_y_coord[index + 1]
		if (y1, y2) not in big_box_temp:
			crop = img[y1:y2, :]  # not table
			idx = (crop.flatten() < 5)
			temp = sum(idx[:])
			if temp < 2:
				continue
			layout_document(crop, document, rule_base, auto_correct)
			string = pytesseract.image_to_string(crop, lang='vie')
			if auto_correct:
				string = rule_base.correct(string)
			result.append(string + "\n")  # for get text
		else:
			index = 0
			box = list_big_box.pop(0)
			for temp in list_result:
				if IOU(temp[0], box):
					index = index + 1
					table = document.add_table(rows=1, cols=len(temp))
					for i, (x, y, w, h) in enumerate(temp):
						crop = img[y:y + h, x:x + w]
						size = int(crop.shape[0] * 1.5)
						if size < 100:
							size = 100
						crop = imutils.resize(crop, height=size)  ##
						crop = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
						idx = (crop.flatten() < 5)
						temp = sum(idx[:])
						if temp < 2:
							continue
						string = pytesseract.image_to_string(crop, lang='vie')
						if auto_correct:
							string = rule_base.correct(string)
						if len(string) == 0:
							kernel = cv2.getStructuringElement(cv2.MORPH_RECT,
							                                   (3, 3))
							crop = cv2.erode(crop, kernel, iterations=1)
							while size <= 200:
								string = pytesseract.image_to_string(crop,
								                                     lang='eng',
								                                     config='--psm 10')
								if ("l" in string or "I" in string) and len(
										string) < 3:
									string = "1"
								if string.isdigit() or (len(
										string) >= 2 and "," not in string and "'" not in string):
									break
								size = size + 10
								crop = imutils.resize(crop, height=size)
						string = string + " "
						string = string.replace("\n", " ")
						row_cells = table.rows[0].cells
						p = row_cells[i].add_paragraph(string)
						p.alignment = WD_TABLE_ALIGNMENT.CENTER
						result.append(string)  # for get text
					result.append("\n")  # for get text
				else:
					break
			list_result = list_result[index:]
	document.save(doc_name)
	return result


def get_text(list_result, list_big_box, img, rule_base, auto_correct=True):
	result = []
	(height, _) = img.shape[:2]
	if len(list_big_box) == 0:
		result.append(pytesseract.image_to_string(img, lang='vie') + "\n")
		return result
	big_box_temp = []
	list_y_coord = [0]
	for (_, y, _, h) in list_big_box:
		big_box_temp.append((y, y + h))
		list_y_coord.append(y)
		list_y_coord.append(y + h)
	list_y_coord.append(height)
	for index, y1 in enumerate(list_y_coord):
		if index == len(list_y_coord) - 1:
			break
		y2 = list_y_coord[index + 1]
		if (y1, y2) not in big_box_temp:
			crop = img[y1:y2, :]
			idx = (crop.flatten() < 5)
			temp = sum(idx[:])
			if temp < 2:
				continue
			result.append(pytesseract.image_to_string(crop, lang='vie') + "\n")
		else:
			index = 0
			box = list_big_box.pop(0)
			for temp in list_result:
				if IOU(temp[0], box):
					index = index + 1
					for (x, y, w, h) in temp:
						crop = img[y:y + h, x:x + w]
						size = int(crop.shape[0] * 1.5)
						if size < 100:
							size = 100
						crop = imutils.resize(crop, height=size)  ##
						crop = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
						idx = (crop.flatten() < 5)
						temp = sum(idx[:])
						if temp < 2:
							continue
						string = pytesseract.image_to_string(crop, lang='vie')
						if len(string) == 0:
							kernel = cv2.getStructuringElement(cv2.MORPH_RECT,
							                                   (3, 3))
							crop = cv2.erode(crop, kernel, iterations=1)
							while size <= 200:
								string = pytesseract.image_to_string(crop,
								                                     lang='eng',
								                                     config='--psm 10')
								if ("l" in string or "I" in string) and len(
										string) < 3:
									string = "1"
								if string.isdigit() or (len(
										string) >= 2 and "," not in string and "'" not in string):
									break
								size = size + 10
								crop = imutils.resize(crop, height=size)
						string = string + " "
						string = string.replace("\n", " ")
						result.append(string)
					result.append("\n")
				else:
					break
			list_result = list_result[index:]
	return result
