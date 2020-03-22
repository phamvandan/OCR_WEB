import os

from PyPDF2 import PdfFileReader
from pdf2image import convert_from_path


def pdf_to_images(pdf_file, output_folder, save_image):
	print("Converting PDF to Images......")
	i = 1
	pdf = PdfFileReader(open(str(pdf_file), 'rb'))
	max_pages = pdf.getNumPages()
	for page in range(1, max_pages + 1, 10):
		images_from_path = convert_from_path(pdf_file, dpi=200, first_page=page,
		                                     last_page=min(page + 10 - 1,
		                                                   max_pages))
		if save_image:
			for image in images_from_path:
				# print(output_folder)
				try:
					image.save(
						os.path.join(str(output_folder), str(i) + '.jpg'))
				except:
					print('Error when make images from pdf')
					print('Error file ' + str(pdf_file))
				i = i + 1
	return max_pages, images_from_path
