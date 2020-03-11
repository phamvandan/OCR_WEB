import pytesseract
from utils.handleTable import IOU,printImage
import cv2
import imutils
import numpy as np
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
import os

def checkIOUwithAboveRow(cell1,cell2):
    (x,y,w,h) = cell1
    (x1,y1,w1,h1) = cell2
    if (y1<=y and y<=y1+h1-5) or (y<=y1 and y+h-5>=y1):
        return True
    return False

def checkIOUwithAboveCell(cell1,cell2):
    (x,y,w,h) = cell1
    (x1,y1,w1,h1) = cell2
    if (x<=x1 and x1<=x+w) or (x1<=x and x <= x1+w1):
        return True
    return False

def getStringFromImage(box,image):
    (x,y,w,h) = box
    crop = image[y:y+h,x:x+w]
    string = pytesseract.image_to_string(crop,lang='vie')
    cv2.rectangle(image, (x, y), (x + w, y + h), 255, 1)
    return string

def layoutDocument(image,document):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    # assign a rectangle kernel size
    kernel = np.ones((5, 5), 'uint8')
    par_img = cv2.dilate(thresh, kernel, iterations=5)
    cv2.circle(image, (image.shape[1]//3,10), 4, (0,0,255), 2)
    # printImage(image)
    # printImage(par_img)
    if imutils.is_cv2() or imutils.is_cv4():
        (conts, hierarchy) = cv2.findContours(par_img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    elif imutils.is_cv3():
        (_, conts, hierarchy) = cv2.findContours(par_img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    listResult = []
    if len(conts) > 0:
        conts = imutils.contours.sort_contours(conts)[0]
        for i in range(len(conts)):
            (x, y, w, h) = cv2.boundingRect(conts[i])
            if w<25 or h <25 or abs(image.shape[1]-w-x)<=10 or x<=5 or (w <50 and h < 50):
                # print("over")
                continue
            skip = False
            for index,temp in enumerate(listResult):
                for index1,box in enumerate(temp):
                    if IOU(box,(x,y,w,h)):
                        ## if new box is bigger
                        if w*h>box[2]*box[3]:
                            listResult[index][index1] = (x,y,w,h)
                        skip = True
                        break
            if skip == False:
                over = False
                for index,temp in enumerate(listResult):
                    (x1,y1,w1,h1) = temp[0]
                    if abs(y1-y)<=5 or (checkIOUwithAboveRow(temp[0],(x,y,w,h)) and x>=(temp[len(temp)-1][0]+temp[len(temp)-1][2])):
                        listResult[index].append((x,y,w,h))
                        over = True
                if over == False:
                    listResult.append([(x,y,w,h)])
        ## sort
    for index,_ in enumerate(listResult):
        listResult[index] = sorted(listResult[index], key=lambda x: x[0])
    listResult = sorted(listResult,key=lambda x: x[0][1])
    for index,temp in enumerate(listResult):
        for (x,y,w,h) in temp:
            cv2.rectangle(image, (x, y), (x + w, y + h), 255, 1)
        # printImage(image)
    # index = 0
    # while index < len(listResult):
    #     temp = listResult[index]
    #     if index>0:
    #         for index2,boxbelow in enumerate(temp):
    #             (x,y,w,h) = boxbelow
    #             for index1,box in enumerate(listResult[index-1]):
    #                 (x1,y1,w1,h1) = box
    #                 dis = y - (y1+h1)
    #                 if dis >=0 and dis<=3 and checkIOUwithAboveCell(box,boxbelow): ## concat box
    #                     listResult[index-1][index1] = (min(x,x1),y1,max(w1,w),h1+h+dis)
    #                     listResult[index].pop(index2)
    #                     if len(listResult[index])==0:
    #                         listResult.pop(index)
    #                         index = index - 1
    #                     print("concat box success")
    #                     # break
    #     index = index + 1
    lenlist = len(listResult)
    for k,temp in enumerate(listResult):
        align = WD_TABLE_ALIGNMENT.CENTER
        if len(temp) == 1:
            (x,y,w,h) = temp[0]
            if (x<image.shape[1]/5 or (w > image.shape[1]/2 and x<image.shape[1]/3)) and k != 1: ## kiem tra align
                align = WD_TABLE_ALIGNMENT.LEFT
                # print("left")
            elif x>image.shape[1]/2:
                listResult[k].insert(0,(0,0,0,0))
                
        table = document.add_table(rows=1, cols=len(temp))
        row_cells = table.rows[0].cells
        for index,(x,y,w,h) in enumerate(temp):
            if (x,y,w,h) == (0,0,0,0):
                string = ""
                p = row_cells[index].add_paragraph(string)
                p.alignment = align
                continue
            string = getStringFromImage((x,y,w,h),image)
            p = row_cells[index].add_paragraph(string)
            p.alignment = align
    return listResult,document    

def GetTextLayout(listResult,listBigBox,img,docName):
    ## open or create docx file
    if os.path.exists(docName) == False:
        dc = Document()
        dc.save(docName)
    document = Document(docName)

    result = []
    (height,_) = img.shape[:2]
    if len(listBigBox)==0:
        layoutDocument(img,document)
        document.save(docName)
        result.append(pytesseract.image_to_string(img,lang='vie')+"\n")
        return result
    bigBoxTemp = []
    listYCoord = []
    listYCoord.append(0)
    for (_,y,_,h) in listBigBox:
        bigBoxTemp.append((y,y+h))
        listYCoord.append(y)
        listYCoord.append(y+h)
    listYCoord.append(height)
    for index,y1 in enumerate(listYCoord):
        if index == len(listYCoord)-1:
            break
        y2 = listYCoord[index+1]
        if (y1,y2) not in bigBoxTemp:
            crop = img[y1:y2,:] # not table
            idx = (crop.flatten()<5)
            temp = sum(idx[:])
            if temp <2:
                continue
            layoutDocument(crop,document)
            result.append(pytesseract.image_to_string(crop,lang='vie')+"\n")  # for get text
        else:
            index = 0
            box = listBigBox.pop(0)
            for temp in listResult:
                if IOU(temp[0],box):
                    index = index +1
                    table = document.add_table(rows=1, cols=len(temp))
                    for i,(x,y,w,h) in enumerate(temp):
                        crop = img[y:y+h,x:x+w]
                        size = int(crop.shape[0]*1.5)
                        if size < 100:
                            size = 100
                        crop = imutils.resize(crop,height=size) ## 
                        crop = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
                        idx = (crop.flatten()<5)
                        temp = sum(idx[:])
                        if temp <2:
                            continue
                        string  = pytesseract.image_to_string(crop,lang='vie')
                        if len(string) == 0:
                            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
                            crop = cv2.erode(crop, kernel, iterations=1)
                            while size<=200:
                                string  = pytesseract.image_to_string(crop,lang='eng',config='--psm 10')
                                if ("l" in string or "I" in string ) and len(string)<3:
                                    string = "1"
                                if string.isdigit() or (len(string)>=2 and "," not in string and "'" not in string):
                                    break
                                size = size + 10
                                crop = imutils.resize(crop,height=size)
                        string = string + " "
                        string = string.replace("\n"," ")
                        row_cells = table.rows[0].cells
                        p = row_cells[i].add_paragraph(string)
                        p.alignment = WD_TABLE_ALIGNMENT.CENTER
                        result.append(string) #for get text
                    result.append("\n") #for get text
                else:
                    break
            listResult = listResult[index:]
    document.save(docName)
    return result
    
def GetText(listResult,listBigBox,img):
    result = []
    (height,_) = img.shape[:2]
    if len(listBigBox)==0:
        result.append(pytesseract.image_to_string(img,lang='vie')+"\n")
        return result
    bigBoxTemp = []
    listYCoord = []
    listYCoord.append(0)
    for (_,y,_,h) in listBigBox:
        bigBoxTemp.append((y,y+h))
        listYCoord.append(y)
        listYCoord.append(y+h)
    listYCoord.append(height)
    for index,y1 in enumerate(listYCoord):
        if index == len(listYCoord)-1:
            break
        y2 = listYCoord[index+1]
        if (y1,y2) not in bigBoxTemp:
            crop = img[y1:y2,:]
            idx = (crop.flatten()<5)
            temp = sum(idx[:])
            if temp <2:
                continue
            result.append(pytesseract.image_to_string(crop,lang='vie')+"\n")
        else:
            index = 0
            box = listBigBox.pop(0)
            for temp in listResult:
                if IOU(temp[0],box):
                    index = index +1
                    for (x,y,w,h) in temp:
                        crop = img[y:y+h,x:x+w]
                        size = int(crop.shape[0]*1.5)
                        if size < 100:
                            size = 100
                        crop = imutils.resize(crop,height=size) ## 
                        crop = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
                        idx = (crop.flatten()<5)
                        temp = sum(idx[:])
                        if temp <2:
                            continue
                        string  = pytesseract.image_to_string(crop,lang='vie')
                        if len(string) == 0:
                            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
                            crop = cv2.erode(crop, kernel, iterations=1)
                            while size<=200:
                                string  = pytesseract.image_to_string(crop,lang='eng',config='--psm 10')
                                if ("l" in string or "I" in string ) and len(string)<3:
                                    string = "1"
                                if string.isdigit() or (len(string)>=2 and "," not in string and "'" not in string):
                                    break
                                size = size + 10
                                crop = imutils.resize(crop,height=size)
                        string = string + " "
                        string = string.replace("\n"," ")
                        result.append(string)
                    result.append("\n")
                else:
                    break
            listResult = listResult[index:]
    return result