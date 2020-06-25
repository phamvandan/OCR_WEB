import os

dir_path = 'data/no_table/tesseract/'
# dir_path = 'data/no_table/our_method/'
# dir_path = 'data/no_table/corrected/'
# dir_path = 'data/table/tesseract/'
# dir_path = 'data/table/our_method/'
# dir_path = 'data/table/corrected/'

files = os.listdir(dir_path)
for file in files:
	path_to_file = os.path.join(dir_path, file)
	with open(path_to_file, 'r') as f:
		text = f.read()
		text = ' '.join(text.split())
		path_to_save = os.path.join('data/no_table/tesseract_regex/', file)
		# path_to_save = os.path.join('data/no_table/our_method_regex/', file)
		# path_to_save = os.path.join('data/no_table/corrected_regex/', file)
		# path_to_save = os.path.join('data/table/tesseract_regex/', file)
		# path_to_save = os.path.join('data/table/our_method_regex/', file)
		# path_to_save = os.path.join('data/table/corrected_regex/', file)
		with open(path_to_save, 'w+') as fw:
			fw.write(text)
