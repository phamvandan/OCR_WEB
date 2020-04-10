import os
import tempfile
from pathlib import Path

from pdf2image import convert_from_path


def pdf_to_images(pdf_file, output_folder, save_image):
	print("Converting PDF to Images......")
	i = 1

	with tempfile.TemporaryDirectory() as path:
		images_from_path = convert_from_path(pdf_file, dpi=200, fmt='jpeg',
		                                     output_folder=path)
		if save_image:
			path = Path(pdf_file)
			path_to_folder_save = os.path.join(str(output_folder),
			                                   path.stem.split('.')[0])
			if not os.path.exists(path_to_folder_save):
				os.makedirs(path_to_folder_save)
			for image in images_from_path:
				try:
					image.save(
							os.path.join(path_to_folder_save, str(i) + '.jpg'))
				except:
					print('Error when make images from pdf')
					print('Error file ' + str(pdf_file))
				i = i + 1
	return images_from_path
# pdf = PdfFileReader(open(str(pdf_file), 'rb'))
# max_pages = pdf.getNumPages()
# images = []
# for page in range(1, max_pages + 1, 10):
# 	images_from_path = convert_from_path(pdf_file, dpi=200, first_page=page,
# 	                                     last_page=min(page + 10 - 1,
# 	                                                   max_pages))
# 	for image in images_from_path:
# 		# print(output_folder)
# 		images.append(image)
# 		if save_image:
# 			try:
# 				image.save(
# 					os.path.join(str(output_folder), str(i) + '.jpg'))
# 			except:
# 				print('Error when make images from pdf')
# 				print('Error file ' + str(pdf_file))
# 			i = i + 1
# return max_pages, images

# i = 1
# pages = convert_from_path(pdf_file, dpi=200)
# for page in pages:
# 	if save_image:
# 			try:
# 				page.save(
# 						os.path.join(str(output_folder), str(i) + '.jpg'))
# 			except:
# 				print('Error when make images from pdf')
# 				print('Error file ' + str(pdf_file))
# 			i = i + 1
# return i-1, pages
