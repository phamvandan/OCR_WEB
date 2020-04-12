from utils.skew_process.rotation import rotateAndScale
from utils.skew_process.skew_detect import SkewDetect
import re
import pytesseract
import cv2,imutils
import numpy as np
def h_v_detect(image):
    if len(image.shape) == 2:
        gray_img = image
    elif len(image.shape) == 3:
        gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # #print(gray_img.shape)
    thresh_img = cv2.adaptiveThreshold(~gray_img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, -2)
    # cv2.imwrite('thresh_img.jpg',thresh_img)
    h_img = thresh_img.copy()
    v_img = thresh_img.copy()
    scale = 15
    h_size = int(h_img.shape[1] / scale)

    h_structure = cv2.getStructuringElement(cv2.MORPH_RECT,
                                            (h_size, 1))  # 形态学因子
    h_erode_img = cv2.erode(h_img, h_structure, 1)
    h_dilate_img = cv2.dilate(h_erode_img, h_structure, 1)
    v_size = int(v_img.shape[0] / scale)
    v_structure = cv2.getStructuringElement(cv2.MORPH_RECT,
                                            (1, v_size))  # 形态学因子
    v_erode_img = cv2.erode(v_img, v_structure, 1)
    v_dilate_img = cv2.dilate(v_erode_img, v_structure, 1)
    mask_img = h_dilate_img + v_dilate_img
    mask_img = ~mask_img
    mask_img[mask_img>0]=1
    # #print("mask value",mask_img[:2])
    return mask_img

def remove_line(img):
    mask_image = h_v_detect(img)
    #print_image(img)
    mask_image_stacked = np.stack((mask_image,)*3,axis=-1)
    #print(mask_image_stacked.shape)
    img = ~img*mask_image_stacked
    img = ~img
    return img

class Deskew:

	def __init__(self, image, r_angle=0):
		self.image = image
		self.r_angle = r_angle
		self.skew_obj = SkewDetect(input_file=self.image)

	def deskew(self):
		img = self.image.copy()
		(h, w) = img.shape[:2]
		print(h, w)
		(h, w) = img.shape[:2]
		if w > 1000:
			if w > 2000:
				img = imutils.resize(img, width=1200)
			else:
				img = imutils.resize(img, width=1000)
		img = remove_line(img)

		res = self.skew_obj.process_single_file(img)
		angle = res['Estimated Angle']
		print("estimate angle",angle)
		if 0 <= angle <= 90:
			rot_angle = angle - 90 + self.r_angle
		if -45 <= angle < 0:
			rot_angle = angle - 90 + self.r_angle
		if -90 <= angle < -45:
			rot_angle = 90 + angle + self.r_angle

		rotated = rotateAndScale(img, rot_angle)
		if rotated.shape[1]<1000:
			rotated = imutils.resize(rotated,width=1000)
		try:
			new_data = pytesseract.image_to_osd(rotated)
			angle = re.search('(?<=Rotate: )\d+', new_data).group(0)
			angle = float(angle)
		except:
			angle = 0
		rot_angle = rot_angle + angle
		rotated = rotateAndScale(self.image, rot_angle)
		return rotated, rot_angle

	def run(self):
		if self.image is not None:
			return self.deskew()
