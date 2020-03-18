import os

from PyPDF2 import PdfFileReader
from pdf2image import convert_from_path


def pdfToImage(pdf_file, output_folder):
	"""

	"""
	print("Converting PDF to Images......")
	i = 1
	try:
		pdf = PdfFileReader(open(str(pdf_file), 'rb'))
	except:
		return None
		maxPages = pdf.getNumPages()
		for page in range(1, maxPages + 1, 10):
			images_from_path = convert_from_path(pdf_file, dpi=200, first_page=page,
			                                     last_page=min(page + 10 - 1, maxPages))
			for image in images_from_path:
				# print(output_folder)
				try:
					image.save(os.path.join(str(output_folder), str(i) + '.jpg'))
				except:
					print()
				i = i + 1
		return maxPages
