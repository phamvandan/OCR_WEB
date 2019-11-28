import cv2, pytesseract, pdf2image, os
from utils.DetectTable import detectTable
from utils.skew import skewImage
from utils.handleTable import getTableCoordinate, retreiveTextFromTable
from utils.PdfToImages import pdfToImage
from pathlib import Path

def handleFile(fileName,deblur=False,handleTableBasic=True,handleTableAdvance=False):
    """
    :param fileName: name of image to be converted
    :param outputName: name of doc file to be saved
    :return:

    detect table and layout-analyzing
    """
    img = cv2.imread(fileName)
    # handle skew
    img = skewImage(img)
    # skew.printImage(img)
    # handle table with not auto fill
    resultTable =''
    if handleTableBasic or handleTableAdvance:
        if handleTableBasic:
            mask = detectTable(img).run(1)
        else:
            mask = detectTable(img).run(2)
        # maskName = "mask.jpg"
        # mask_img = cv2.imread(maskName)
        mask_img = mask
        print(mask.shape)
        ## resize
        listResult, listBigBox = getTableCoordinate(mask_img)
        img = cv2.resize(img, (mask_img.shape[1], mask_img.shape[0]))
        # origin = img.copy()
        resultTable = retreiveTextFromTable(listResult,img)
        for pt in listBigBox:
            (x, y, w, h) = pt
            if w > 0.9*img.shape[1]:
                continue
            # cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,0),2)
            img[y:(y + h - 1), x:(x + w - 1)] = 255
        # out, result = handleTable.process_par(img, origin, listBigBox) ## use for layout
    # skew.printImage(img)
    # resultNotTable = pytesseract.image_to_string(img,lang="vie")
    resultNotTable = pytesseract.image_to_string(img,lang="vie")
    return resultNotTable,resultTable

def saveResult(folder,saveFileName,result):
    file  = os.path.join(str(folder),saveFileName)
    if os.path.exists(file):
        f = open(file,"a+")
    else:
        f = open(file,"w+")
    f.write(result)
    f.close()

def getFileName(fileType,folder):
    names = []
    if fileType == "pdf":
        count = 0
        for filename in os.listdir(folder):
            if "pdf" in filename:
                filename = os.path.join(str(folder0,filename)
                print(filename)
                count = pdfToImage(filename,folder) ## convert to image
        for k in range(1,count+1):
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

def preprocessFile(fileType,folder,saveFileName):
    names = getFileName(fileType,folder)
    result = ""
    if fileType == "pdf" or fileType == "image":
        for filename in names:
            filename = os.path.join(folder,filename)
            if ".jpg" in filename:
                resultNotTable,resultTable = handleFile(filename,deblur=False,handleTableBasic=False,handleTableAdvance=True)
                result= result + (str(resultNotTable))
                k = 0
                for rs in resultTable:
                    if k %4 == 0:
                        result = result + "\n"
                    result= result + (str(rs))+" "
                    k = k+ 1
                if fileType == "pdf":
                    os.remove(filename)
    elif fileType=="text":
        for filename in names:
            filename = os.path.join(folder,filename)
            f = open(filename,"r")
            result = result + str(f.read())
            f.close()
    if result != "":
        saveResult(folder,saveFileName,result)
    return result
def processPdfFile(folder_in, folder_out, folder_out_1):
    fileType = "pdf"
    iD= 1
    for r, d, f in os.walk(folder_in):
        for file in f:
            if file.__contains__(fileType):
                if(os.path.exists(os.path.join(folder_in,"state"+Path(file).stem+".txt"))):
                    continue
                print(str(iD)+"--"+file)
                iD = iD +1
                names = []
                count = 0
                result = ""
                filename = os.path.join(r, file)
                count = pdfToImage(filename, folder_in) ## convert to image
                for k in range(1,count+1):
                    names.append(str(k)+".jpg")
                for filename in names:
                    filename = os.path.join(folder_in, filename)
                    if ".jpg" in filename:
                        
                        result= result + (str(resultNotTable))
                        
                    if fileType == "pdf":
                        os.remove(filename)
                if result != "":
                    saveResult(folder_out, Path(file).stem+".txt",result)
                    saveResult(folder_out_1, Path(file).stem+".txt",result)
                    saveResult(folder_in, "state"+Path(file).stem+".txt", "None")

def tesseractPdf(folder_in, folder_out):
    fileType = "pdf"
    iD= 1
    for r, d, f in os.walk(folder_in):
        for file in f:
            if file.__contains__(fileType):
                if(os.path.exists(os.path.join(folder_out,Path(file).stem+".txt"))):
                    continue
                print(str(iD)+"--"+file)
                iD = iD +1
                names = []
                count = 0
                result = ""
                filename = os.path.join(r, file)
                count = pdfToImage(filename, folder_in) ## convert to image
                for k in range(1,count+1):
                    names.append(str(k)+".jpg")
                for filename in names:
                    filename = os.path.join(folder_in, filename)
                    if ".jpg" in filename:
                        img = cv2.imread(filename)
                        rs = pytesseract.image_to_string(img,lang="vie")
                        result= result + rs
                    if fileType == "pdf":
                        os.remove(filename)
                if result != "":
                    saveResult(folder_out, Path(file).stem+".txt",result)