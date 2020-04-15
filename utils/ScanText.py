import os

import cv2
import imutils
import numpy as np
import pytesseract
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT

from utils.table_process.find_bb import IOU
from utils.main import entry_dla


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


def get_text_layout(list_result, list_big_box, img, doc_name, rule_base,
                    auto_correct=True):
    ## open or create docx file
    if not os.path.exists(doc_name):
        dc = Document()
        dc.save(doc_name)
    document = Document(doc_name)
    result = []
    (height, _) = img.shape[:2]
	# if not have table
    if len(list_big_box) == 0:
        string = entry_dla(img, document, rule_base, auto_correct)
        document.save(doc_name)
        # string = pytesseract.image_to_string(img, lang='vie')
        # if auto_correct:
        # 	string = rule_base.correct(string)
        result.append(string + "\n")
        return result
	## if have table
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
            string = entry_dla(crop, document, rule_base, auto_correct)
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
