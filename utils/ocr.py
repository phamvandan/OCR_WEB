import os
import time
from pathlib import Path

import cv2
import numpy
from docx import Document

from utils import config_file as cf
from utils.ScanText import get_text, get_text_layout
from utils.pdf_to_images import pdf_to_images
from utils.skew_process.deskew import Deskew
from utils.table_process.DetectTable import DetectTable
from utils.table_process.find_bb import get_table_coordinate
from utils.text_correction.RuleBase import RuleBase

pdfExtension = [".pdf", ".PDF"]
imageExtension = [".jpg", ".JPG", ".png", ".PNG"]


class OcrFile:
	def __init__(self, file_path, skew_mode=False, table_mode=0,
	             auto_correct_mode=False, make_docx_file=False, make_txt=False):
		"""
		:param file_path: path to file ocr
		:type file_path: str
		:param skew_mode: True for using deskew
		:type skew_mode: bool
		:param table_mode:0 without auto fill talbe, 1 with auto fill table
		:type table_mode: int
		:param auto_correct_mode: True for auto correct text
		:type auto_correct_mode: bool
		:param make_docx_file: True for generate docx file
		:type make_docx_file: bool
		:param make_txt: True for generate txt file
		:type make_txt: bool
		"""
		self.file_path = Path(file_path)
		self.file_name = self.file_path.stem
		self.images = []
		self.mask_images = []
		self.list_result = []
		self.list_big_box = []
		self.text = ''
		self.make_docx_file = make_docx_file
		self.skew_mode = skew_mode
		self.table_mode = table_mode
		self.auto_correct_mode = auto_correct_mode
		self.make_txt = make_txt
		self.number_images = 0
		self.debug_directory = "utils/save_image/"
		if not os.path.isdir(self.debug_directory):
			os.mkdir(self.debug_directory)
		# self.path_to_images = []
		self.extension = self.file_path.suffix
		if self.extension.lower() == '.pdf':
			self.type = 'pdf'
			print('File type : PDF')
		elif self.extension.lower() in ['.jpg', '.png']:
			self.type = 'image'
			self.number_images = 1
			# print('File type : Image')
		elif self.extension.lower() == '.docx':
			self.type = 'docx'
			print('File type : docx')
		else:
			self.type = None
			print('Unknown File type')

	def run(self):
		if self.type is not None:
			self.convert_to_images(cf.save_image)
			if self.type in ['pdf', 'image']:
				if self.skew_mode:
					self.deskew()
				self.process_table()
				self.get_text_and_make_docx()
				# if self.auto_correct_mode:
				# 	rule_base = RuleBase()
				# 	self.text = rule_base.correct(self.text)
				if self.make_txt:
					path_to_txt = os.path.splitext(self.file_path)[0] + '.txt'
					if os.path.isfile(str(path_to_txt)):
						os.remove(path_to_txt)
					with open(path_to_txt, 'w+') as f:
						while True:
							text1 = self.text
							self.text = self.text.replace("\n\n", "\n")
							self.text = self.text.replace("\n \n", "\n")
							if self.text.endswith(text1):
								break
						# print(self.text)
						f.write(self.text)
			else:
				# process dpf
				return
		else:
			print('Error file!!!')
		return self.text

	def convert_to_images(self, save_image=False):
		t = time.time()
		if self.type == 'pdf':
			self.images = pdf_to_images(self.file_path,
			                            self.debug_directory,
			                            save_image)
			self.number_images = len(self.images)
		# for k in range(1, self.number_images + 1):
		# 	path_to_image = os.path.join(self.debug_directory,
		# 	                             self.file_name + str(k) + '.jpg')
		# 	self.path_to_images.append(path_to_image)
		elif self.type == 'image':
			# print(self.file_path)
			img = cv2.imread(str(self.file_path))
			self.images.append(img)
			self.number_images = 1
		elif self.type == 'docx':
			doc = Document(self.file_path)
			full_text = []
			for para in doc.paragraphs:
				full_text.append(para.text)
			self.text = full_text
		# if save_image:
		# 	print(
		# 			'Convert to images take ' + '{0:.2f}'.format(
		# 					time.time() - t))

	def deskew(self):
		t = time.time()
		if self.type == 'docx':
			return
		else:
			# print(self.number_images, len(self.images))
			for i in range(0, self.number_images):
				# print(i)
				image = numpy.array(self.images[i])
				image_after_deskew, _ = Deskew(image).run()
				self.images[i] = image_after_deskew
		if cf.calculate_time:
			print('Deskew take ' + '{0:.2f}'.format(time.time() - t))
	## khong co viec gi kho
	def process_table(self):
		t = time.time()
		for i in range(0, self.number_images):
			# print(self.table_mode)
			mask_image = DetectTable(self.images[i]).run(
					self.table_mode)
			self.mask_images.append(mask_image)
			list_result, list_big_box = get_table_coordinate(
					self.mask_images[i])
			# print("list result\n",list_result)
			# print("list big box\n",list_big_box)
			self.list_result.append(list_result)
			self.list_big_box.append(list_big_box)
			# self.images[i] = cv2.resize(self.images[i], (
			# 	self.mask_images[i].shape[1], self.mask_images[i].shape[0]))
		if cf.calculate_time:
			print('Process table take ' + '{0.2f}'.format(time.time() - t))

	def get_text_and_make_docx(self):
		t = time.time()
		rule_base = RuleBase()
		for i in range(0, self.number_images):
			text = ""
			if not self.make_docx_file:
				text = get_text(self.list_result[i],
				                        self.list_big_box[i],
				                        self.images[i], rule_base,
				                        self.auto_correct_mode)
			else:
				file_docx = os.path.splitext(self.file_path)[0]
				text = get_text_layout(self.list_result[i],
				                               self.list_big_box[i],
				                               self.images[i],
				                               file_docx + '.docx', rule_base,
				                               self.auto_correct_mode)
			self.text = self.text + text
		if cf.calculate_time:
			print('Get text and make docx take ' + '{0:.2f}'.format(
					time.time() - t))
