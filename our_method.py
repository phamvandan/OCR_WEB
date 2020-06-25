import os
from utils.ocr import OcrFile
import numpy as np
import cv2

# path = 'data/no_table/image_skew/'
path = 'data/table/image/'
list_subfolders_with_paths = [f.path for f in os.scandir(path) if f.is_dir()]
for subfolder in list_subfolders_with_paths:
	# if subfolder == 'utils/save_image/188':
	print(subfolder)
	images = os.listdir(subfolder)
	print(images)
	for image in images:
		path_to_image = os.path.join(subfolder, image)
		print(path_to_image)
		# path_to_txt = os.path.join('data/no_table/our_method/',
		#                            subfolder.split('/')[-1] + "_" +
		#                            image.split('.')[0] + '.txt')
		path_to_txt = os.path.join('data/table/our_method/',
		                           subfolder.split('/')[-1] + "_" +
		                           image.split('.')[0] + '.txt')
		print(path_to_txt)
		if os.path.isfile(path_to_txt):
			continue
		ocr= OcrFile(path_to_image,True, 0, True, False, False)
		result = ocr.run()
		# path_to_txt = os.path.join('data/no_table/our_method/', subfolder.split('/')[-1]+"_"+image.split('.')[0]+'.txt')

		with open(path_to_txt, 'w+') as file:
			file.write(result)