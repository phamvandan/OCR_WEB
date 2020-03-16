""" Deskews file after getting skew angle """
import optparse
import numpy as np
import matplotlib.pyplot as plt
import sys
import os

from utils.skew_detect import SkewDetect
# from skimage import io
# from skimage.transform import rotate
from utils.rotation import rotateAndScale

import pytesseract
import re
import imutils


class Deskew:

    def __init__(self, image, r_angle=0):
        self.image = image
        self.r_angle = r_angle
        self.skew_obj = SkewDetect(input_file=self.image)

    def deskew(self):
        ### change here
        img = self.image.copy()
        (h, w) = img.shape[:2]
        if w > 800:
            img = imutils.resize(img, width=800)
        (h, w) = img.shape[:2]
        res = self.skew_obj.process_single_file(img)
        angle = res['Estimated Angle']

        if angle >= 0 and angle <= 90:
            rot_angle = angle - 90 + self.r_angle
        if angle >= -45 and angle < 0:
            rot_angle = angle - 90 + self.r_angle
        if angle >= -90 and angle < -45:
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
