from difflib import SequenceMatcher
from random import randint, seed
import numpy as np
import cv2
import pytesseract
import matplotlib.pyplot as plt
from utils.skew_process.rotation import rotateAndScale
import os
from utils.ocr import OcrFile
import cv2
from jiwer import wer

def rotate(angle):
    path = 'data/no_table/image/'
    path_save = 'data/no_table/image_skew/'
    list_subfolders_with_paths = [f.path for f in os.scandir(path) if
                                  f.is_dir()]
    for subfolder in list_subfolders_with_paths:
        path_to_subfolder = os.path.join(path_save, subfolder.split('/')[-1])
        if not os.path.exists(path_to_subfolder):
            os.makedirs(path_to_subfolder)
        images = os.listdir(subfolder)
        for image in images:
            path_to_origin = os.path.join(subfolder, image)
            path_to_save = os.path.join(path_to_subfolder, image)
            img = cv2.imread(path_to_origin)
            img = rotateAndScale(img, angle)
            cv2.imwrite(path_to_save, img)
def our_method():
    path = 'data/no_table/image_skew/'
    list_subfolders_with_paths = [f.path for f in os.scandir(path) if
                                  f.is_dir()]
    for subfolder in list_subfolders_with_paths:
        # if subfolder == 'utils/save_image/188':
        # print(subfolder)
        images = os.listdir(subfolder)
        # print(images)
        for image in images:
            path_to_image = os.path.join(subfolder, image)
            # print(path_to_image)
            path_to_txt = os.path.join('data/no_table/our_method/',
                                       subfolder.split('/')[-1] + "_" +
                                       image.split('.')[0] + '.txt')
            # print(path_to_txt)
            ocr = OcrFile(path_to_image, True, 0, True, False, False)
            result = ocr.run()
            with open(path_to_txt, 'w+') as file:
                file.write(result)
def tesseract():
    path = 'data/no_table/image_skew/'
    list_subfolders_with_paths = [f.path for f in os.scandir(path) if
                                  f.is_dir()]
    for subfolder in list_subfolders_with_paths:
        # print(subfolder)
        images = os.listdir(subfolder)
        # print(images)
        for image in images:
            path_to_image = os.path.join(subfolder, image)
            # print(path_to_image)
            img = cv2.imread(path_to_image)
            img = np.array(img)
            text = pytesseract.image_to_string(img, lang='vie')
            path_to_txt = os.path.join('data/no_table/tesseract/',
                                       subfolder.split('/')[-1] + "_" +
                                       image.split('.')[0] + '.txt')
            # print(path_to_txt)
            with open(path_to_txt, 'w+') as file:
                file.write(text)
def regex(dir_path):
    if dir_path=='data/no_table/tesseract/':
        path = 'data/no_table/tesseract_regex/'
    else:
        path = 'data/no_table/our_method_regex/'
    files = os.listdir(dir_path)
    for file in files:
        path_to_file = os.path.join(dir_path, file)
        with open(path_to_file, 'r') as f:
            text = f.read()
            text = ' '.join(text.split())
            path_to_save = os.path.join(path, file)
            with open(path_to_save, 'w+') as fw:
                fw.write(text)
def calculate_similary():
    corrected_path = 'data/no_table/corrected_regex/'
    our_method_path = 'data/no_table/our_method/'
    tesseract_path = 'data/no_table/tesseract/'
    files = os.listdir(corrected_path)
    # print(files)
    x = []
    y1 = []
    y2 = []
    i = 1
    for file in files:
        path_to_correct = os.path.join(corrected_path, file)
        # print(path_to_correct)
        path_to_our_method = os.path.join(our_method_path, file)
        path_to_tesseract = os.path.join(tesseract_path, file)
        with open(path_to_correct, 'r') as fread:
            correct = fread.read()
        with open(path_to_our_method, 'r') as fread:
            our_method = fread.read()
        with open(path_to_tesseract, 'r') as fread:
            tesseract = fread.read()
        # s1 = SequenceMatcher(lambda x: x == " ", our_method, correct)
        s1 = wer(correct,our_method)
        # s2 = SequenceMatcher(lambda x: x == " ", tesseract, correct)
        s2 = wer(correct, tesseract)
        y1.append(round(s1, 2))
        y2.append(round(s2, 2))
        x.append(i)
        i = i + 1
    y1_np = np.asarray(y1)
    y2_np = np.asarray(y2)
    y1_mean = round(np.mean(y1_np), 2)
    y2_mean = round(np.mean(y2_np), 2)
    return y1_mean, y2_mean
angles = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

for i in range(1, 36):
    angles.append(i * 10)
for angle in angles:
    print(angle)
    print('Rotating')
    rotate(angle)
    print('eDMS running')
    our_method()
    print('tesseract running')
    tesseract()
    regex('data/no_table/tesseract/')
    regex('data/no_table/our_method/')
    y1, y2 = calculate_similary()
    with open('data/no_table/result.txt', 'a+') as f_write:
        f_write.write(str(angle)+'\t'+str(y1)+'\t'+str(y2)+'\n')