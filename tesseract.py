import os

import pytesseract

from utils.ocr import OcrFile
import numpy as np
import cv2

path = 'data/no_table/image_skew/'
# path = 'data/table/image_skew/'
list_subfolders_with_paths = [f.path for f in os.scandir(path) if f.is_dir()]
for subfolder in list_subfolders_with_paths:
    # if subfolder == 'utils/save_image/188':
    print(subfolder)
    images = os.listdir(subfolder)
    print(images)
    for image in images:
        path_to_image = os.path.join(subfolder, image)
        print(path_to_image)
        img = cv2.imread(path_to_image)
        img = np.array(img)
        text = pytesseract.image_to_string(img, lang='vie')
        path_to_txt = os.path.join('data/no_table/tesseract/', subfolder.split('/')[-1]+"_"+image.split('.')[0]+'.txt')
        # path_to_txt = os.path.join('data/table/tesseract/',
        #                            subfolder.split('/')[-1] + "_" +
        #                            image.split('.')[0] + '.txt')
        print(path_to_txt)
        with open(path_to_txt, 'w+') as file:
            file.write(text)
    # text = ''
    # while i<len(images)+1:
    # 	path_to_image = os.path.join(subfolder, str(i)+'.jpg')
    # 	img = cv2.imread(path_to_image)
    # 	img = np.array(img)
    # 	text = text + pytesseract.image_to_string(img, lang='vie')
    # 	i = i+1
    # # print(text)
    # path_to_txt = os.path.join('tesseract',subfolder.split('/')[-1]+'.txt')
    # with open(path_to_txt,'w+') as f:
    # 	f.write(text)