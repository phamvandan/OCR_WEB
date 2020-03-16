import datetime
import argparse
import pytesseract
from PIL import Image
# from PyPDF2 import PdfFileReader
# from imutils import contours
# from pdf2image import convert_from_path
from utils.deskew import Deskew
from utils.DetectTable import detectTable
from utils.handleTable import getTableCoordinate, retreiveTextFromTable, getInput
from utils.ScanText import GetText, GetTextLayout
import os
import time
# import imutils
import cv2
# from docx import Document
from utils.PdfToImages import pdfToImage
from pathlib import Path


def handleFile(fileName, pdfFileName, pdf, docx=False, skew=False, deblur=False, handleTableBasic=True, handleTableAdvance=False):
    """
    :param str fileName: name of image to be converted
    :param str outputName: name of doc file to be saved
    :return:

    detect table and layout-analyzing
    """
    img = cv2.imread(fileName)

    # handle skew
    if skew:
        start = time.time()
        d = Deskew(img)
        img, angle = d.run()
        end = time.time()
        print('deskew take : '+"{0:.2f}".format(end-start))
    # skew.printImage(img)
    # handle table with not auto fill
    if handleTableBasic or handleTableAdvance:
        start = time.time()
        if handleTableBasic:
            mask = detectTable(img).run(1)
        else:
            mask = detectTable(img).run(2)
        end = time.time()
        print('table handle take '+"{0:.2f}".format(end-start))
        mask_img = mask
        ## resize
        start = time.time()
        listResult, listBigBox = getTableCoordinate(mask_img)
        end = time.time()
        print('getTableCoordinate take '+"{0:.2f}".format(end-start))
        # resize image ?
        img = cv2.resize(img, (mask_img.shape[1], mask_img.shape[0]))
        resultTable = ""
        start = time.time()
        if not docx:
            resultTable = GetText(listResult, listBigBox, img)
        else:
            if not pdf:
                fileNamewithoutExtension = os.path.splitext(fileName)[0]
                resultTable = GetTextLayout(
                    listResult, listBigBox, img, fileNamewithoutExtension+".docx")
            else:
                fileNamewithoutExtension = os.path.splitext(pdfFileName)[0]
                resultTable = GetTextLayout(
                    listResult, listBigBox, img, fileNamewithoutExtension+".docx")
        end = time.time()
        print('docx take '+"{0:.2f}".format(end-start))
    return resultTable


def saveResult(folder, saveFileName, result):
    file = os.path.join(str(folder), saveFileName)
    if os.path.exists(file):
        f = open(file, "a+")
    else:
        f = open(file, "w+")
    f.write(result)
    f.close()
    print(str(datetime.datetime.now()) + " Scan successed")


def getFileName(fileType, folder):
    names = []
    if fileType == "pdf":
        count = 0
        for filename in os.listdir(folder):
            print(filename)
            if "pdf" in filename:
                filename = os.path.join(str(folder), filename)
                count = pdfToImage(filename, folder)  # convert to image
        for k in range(1, count+1):
            names.append(str(k)+".jpg")
    else:
        listname = os.listdir(folder)
        if fileType == "image":
            for name in listname:
                if name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                    names.append(name)
        elif fileType == "text":
            for name in listname:
                if name.lower().endswith(('.txt', '.doc', '.docx')):
                    names.append(name)
    return names


def preprocessFile(fileType, folder, saveFileName, skew, blur, basic, advance):
    if skew.lower() == "true":
        skew = True
    else:
        skew = False
    if blur.lower() == "true":
        blur = True
    else:
        blur = False
    if basic.lower() == "true":
        basic = True
    else:
        basic = False
    if advance.lower() == "true":
        advance = True
    else:
        advance = False

    names = getFileName(fileType, folder)
    result = ""

    if "pdf" in fileType or "image" in fileType:
        for filename in names:
            filename = os.path.join(folder, filename)
            if ".jpg" in filename:
                resultTable = handleFile(
                    filename, skew=skew, deblur=blur, handleTableBasic=basic, handleTableAdvance=advance)
                # k = 0
                for rs in resultTable:
                    # if k %4 == 0:
                    #     result = result + "\n"
                    result = result + (str(rs))
                    # k = k+ 1
                if fileType == "pdf":
                    os.remove(filename)
    elif fileType == "text":
        for filename in names:
            filename = os.path.join(str(folder), filename)
            f = open(filename, "r")
            result = result + str(f.read())
            f.close()
    if result != "":
        result = result.replace("'", "")
        result = result.replace("\"", "")
        saveResult(folder, saveFileName, result)


pdfExtension = [".pdf", ".PDF"]
imageExtension = [".jpg", ".JPG", ".png", ".PNG"]


def ocrFile(filepath, docx, skew_mode, deblur_mode, basicTable, advanceTable):
    path = Path(filepath)
    filename = path.stem
    extension = path.suffix
    currentFolder = path.parent
    result = ""
    if extension in pdfExtension:
        names = []
        count = 0
        # print(currentFolder)
        count = pdfToImage(path, currentFolder)  # convert to image
        for k in range(1, count+1):
            names.append(str(k)+".jpg")
        for image in names:
            print('Start OCR'+str(image)+'-------------------------------')
            imagepath = os.path.join(str(currentFolder), image)
            start = time.time()
            resultTable = handleFile(imagepath, filepath, True, docx=docx, skew=skew_mode,
                                     deblur=deblur_mode, handleTableBasic=basicTable, handleTableAdvance=advanceTable)
        # k = 0
            end = time.time()
            print('Total time OCR '+str(image) +
                  ' : ' + "{0:.2f}".format(end-start))
            for rs in resultTable:
                # if k %4 == 0:
                #     result = result + "\n"
                result = result + (str(rs))
                # k = k+ 1
            os.remove(imagepath)
    elif extension in imageExtension:
        resultTable = handleFile(filepath, '', False, docx=docx, skew=skew_mode,
                                 deblur=deblur_mode, handleTableBasic=basicTable, handleTableAdvance=advanceTable)
        for rs in resultTable:
                # if k %4 == 0:
                #     result = result + "\n"
                result = result + (str(rs))
                # k = k+ 1
    txtPath = str(os.path.splitext(filepath)[0])+'.txt'
    if os.path.exists(txtPath):
        os.remove(txtPath)
    with open(txtPath, 'w+') as f:
        f.write(result)
    return result
