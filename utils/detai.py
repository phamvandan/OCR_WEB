
from utils.deskew import Deskew
from utils.DetectTable import detectTable
from utils.handleTable import getTableCoordinate
from utils.ScanText import GetText, GetTextLayout
import os
import time
import cv2

from utils.PdfToImages import pdfToImage
from pathlib import Path


def handle_file(file_name, pdf_file_name, pdf, docx=False, skew=False, handle_table_basic=True,
                handle_table_advance=False):
    img = cv2.imread(file_name)

    # handle skew
    if skew:
        start = time.time()
        d = Deskew(img)
        img, angle = d.run()
        end = time.time()
        print('deskew take : ' + "{0:.2f}".format(end - start))
    # handle table with not auto fill
    if handle_table_basic or handle_table_advance:
        start = time.time()
        if handle_table_basic:
            mask = detectTable(img).run(1)
        else:
            mask = detectTable(img).run(2)
        end = time.time()
        print('table handle take ' + "{0:.2f}".format(end - start))
        mask_img = mask
        start = time.time()
        listResult, listBigBox = getTableCoordinate(mask_img)
        end = time.time()
        print('getTableCoordinate take ' + "{0:.2f}".format(end - start))
        img = cv2.resize(img, (mask_img.shape[1], mask_img.shape[0]))
        result_table = ""
        start = time.time()
        if not docx:
            result_table = GetText(listResult, listBigBox, img)
        else:
            if not pdf:
                file_namewithout_extension = os.path.splitext(file_name)[0]
                result_table = GetTextLayout(
                        listResult, listBigBox, img, file_namewithout_extension + ".docx")
            else:
                file_namewithout_extension = os.path.splitext(pdf_file_name)[0]
                result_table = GetTextLayout(
                        listResult, listBigBox, img, file_namewithout_extension + ".docx")
        end = time.time()
        print('docx take ' + "{0:.2f}".format(end - start))
    return result_table


def get_file_name(file_type, folder):
    names = []
    if file_type == "pdf":
        count = 0
        for filename in os.listdir(folder):
            print(filename)
            if "pdf" in filename:
                filename = os.path.join(str(folder), filename)
                count = pdfToImage(filename, folder)  # convert to image
        for k in range(1, count + 1):
            names.append(str(k) + ".jpg")
    else:
        listname = os.listdir(folder)
        if file_type == "image":
            for name in listname:
                if name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                    names.append(name)
        elif file_type == "text":
            for name in listname:
                if name.lower().endswith(('.txt', '.doc', '.docx')):
                    names.append(name)
    return names


pdfExtension = [".pdf", ".PDF"]
imageExtension = [".jpg", ".JPG", ".png", ".PNG"]


def ocr_file(filepath, docx, skew_mode, basic_table, advance_table):
    path = Path(filepath)
    filename = path.stem
    extension = path.suffix
    current_folder = path.parent
    result = ""
    if extension in pdfExtension:
        names = []
        count = 0
        # print(current_folder)
        count = pdfToImage(path, current_folder)  # convert to image
        for k in range(1, count + 1):
            names.append(str(k) + ".jpg")
        for image in names:
            print('Start OCR' + str(image) + '-------------------------------')
            image_path = os.path.join(str(current_folder), image)
            start = time.time()
            result_table = handle_file(image_path, filepath, True, docx=docx, skew=skew_mode,
                                       handle_table_basic=basic_table,
                                       handle_table_advance=advance_table)
            # k = 0
            end = time.time()
            print('Total time OCR ' + str(image) +
                  ' : ' + "{0:.2f}".format(end - start))
            for rs in result_table:
                # if k %4 == 0:
                #     result = result + "\n"
                result = result + (str(rs))
                # k = k+ 1
            os.remove(image_path)
    elif extension in imageExtension:
        result_table = handle_file(filepath, '', False, docx=docx, skew=skew_mode,
                                   handle_table_basic=basic_table, handle_table_advance=advance_table)
        for rs in result_table:
            # if k %4 == 0:
            #     result = result + "\n"
            result = result + (str(rs))
            # k = k+ 1
    txt_path = str(os.path.splitext(filepath)[0]) + '.txt'
    if os.path.exists(txt_path):
        os.remove(txt_path)
    with open(txt_path, 'w+') as f:
        f.write(result)
    return result
