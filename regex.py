import os

dir_path = 'corrected/'
# dir_path = 'static/demo/'

files = os.listdir(dir_path)
for file in files:
	if file == '2.txt':
		path_to_file = os.path.join(dir_path, file)
		with open(path_to_file, 'r') as f:
			text_from_file = f.read()
			# print(text_from_file)
			text_regex = ' '.join(text_from_file.split())
			print(text_regex.decode('utf-8').lower())
			with open('text_corrected.txt', 'w+') as fw:
				fw.write(text_regex)
