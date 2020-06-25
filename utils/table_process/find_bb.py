import cv2
import imutils
import numpy as np
from imutils import contours


def IOU(old_box, new_box):
	(x1, y1, w1, h1) = old_box
	(x2, y2, w2, h2) = new_box
	cx1 = x1 + w1 / 2
	cx2 = x2 + w2 / 2
	cy1 = y1 + h1 / 2
	cy2 = y2 + h2 / 2
	if x2 <= cx1 <= x2 + w2 and y2 <= cy1 <= y2 + h2:
		return True
	if x1 <= cx2 <= x1 + w1 and y1 <= cy2 <= y1 + h1:
		return True
	return False


def get_table_coordinate(image,scale=2):
	"""

	:param image:
	:return:
	list_result: x, y coordinates of layout 's bounding box
	list_big_box: x, y coordinates of table in image
	"""
	# image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
	kernel = np.ones((3, 3), np.uint8)
	image = cv2.dilate(image, kernel, iterations=1)
	(h1, w1) = image.shape
	blured = cv2.GaussianBlur(image, (3, 3), 0)
	canny_image = cv2.Canny(blured, 100, 250)
	if imutils.is_cv2() or imutils.is_cv4():
		(conts, _) = cv2.findContours(canny_image.copy(),
		                              cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	elif imutils.is_cv3():
		(_, conts, _) = cv2.findContours(
				canny_image.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	list_big_box = []
	list_result = []
	if len(conts) > 0:
		conts = contours.sort_contours(conts)[0]
		# conts = sorted(conts, key=lambda ctr: cv2.boundingRect(ctr)[0] + cv2.boundingRect(ctr)[1] * image.shape[1] )
		for i in range(len(conts)):
			(x, y, w, h) = cv2.boundingRect(conts[i])
			if 10 < w and  w < 0.7 * w1 and h > 10:
				skip = False
				for temp in list_result:
					for box in temp:
						if IOU(box, (x, y, w, h)):
							skip = True
							break
				if not skip:
					over = False
					for index, temp in enumerate(list_result):
						if abs(temp[0][1] - y) <= 5:
							list_result[index].append((x, y, w, h))
							over = True
					if not over:
						list_result.append([(x, y, w, h)])
				# printImage(newimage)
			if w > 10 and h > 50 and w > 0.7 * w1:
				skip = False
				for box in list_big_box:
					if IOU((x, y, w, h), box):
						skip = True
						break
				if not skip:
					list_big_box.append((x, y, w, h))
	## sort
	for index, _ in enumerate(list_result):
		list_result[index] = sorted(list_result[index], key=lambda x: x[0])
	list_result = sorted(list_result, key=lambda x: x[0][1])
	list_big_box = sorted(list_big_box, key=lambda x: x[1])
	for index,temp in enumerate(list_result):
		for index2,_ in enumerate(temp):
			(x,y,w,h) = list_result[index][index2]
			list_result[index][index2] = (x*scale,y*scale,w*scale,h*scale)
	for index,_ in enumerate(list_big_box):
		(x,y,w,h) = list_big_box[index]
		list_big_box[index] = (x*scale,y*scale,w*scale,h*scale)
	#     for (x,y,w,h) in temp:
	#         cv2.rectangle(newimage, (x, y), (x + w, y + h), 255, 1)
	# for (x,y,w,h) in list_big_box:
	#     cv2.rectangle(newimage, (x, y), (x + w, y + h), 255, 1)
	# printImage(newimage)
	return list_result, list_big_box
