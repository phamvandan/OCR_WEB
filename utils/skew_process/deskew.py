import re

import imutils
import pytesseract

from utils.skew_process.rotation import rotateAndScale
from utils.skew_process.skew_detect import SkewDetect


class Deskew:

	def __init__(self, image, r_angle=0):
		self.image = image
		self.r_angle = r_angle
		self.skew_obj = SkewDetect(input_file=self.image)

	def deskew(self):
		img = self.image.copy()
		(h, w) = img.shape[:2]
		if w > 800:
			img = imutils.resize(img, width=800)
		(h, w) = img.shape[:2]
		res = self.skew_obj.process_single_file(img)
		angle = res['Estimated Angle']

		if 0 <= angle <= 90:
			rot_angle = angle - 90 + self.r_angle
		if -45 <= angle < 0:
			rot_angle = angle - 90 + self.r_angle
		if -90 <= angle < -45:
			rot_angle = 90 + angle + self.r_angle

		rotated = rotateAndScale(img, rot_angle)
		try:
			newdata = pytesseract.image_to_osd(rotated)
			angle = re.search('(?<=Rotate: )\d+', newdata).group(0)
			angle = float(angle)
		except:
			angle = 0
		rot_angle = rot_angle + angle
		rotated = rotateAndScale(self.image, rot_angle)
		return rotated, rot_angle

	def run(self):
		if self.image is not None:
			return self.deskew()
