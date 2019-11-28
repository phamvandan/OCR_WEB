import argparse
import pytesseract
from PIL import Image
# from PyPDF2 import PdfFileReader
from imutils import contours
import imutils
# from pdf2image import convert_from_path
import cv2
import numpy as np
import time

# get image coordinate
def get_boxes_coordinate(image):
    image = cv2.resize(image, (361, 500))

def printImage(image):
    cv2.imshow("my image", image)
    key = cv2.waitKey(0)
    if (key == ord('s')):
        cv2.imwrite(str(int(time.time()))+".jpg",image)
    cv2.destroyAllWindows()

def getInput():
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--inputFile", required=True,
                    help="path to image")  # -i để cho viết tắt trước khi truyền tham số còn không thì
    # ap.add_argument("-n","--outName",required = True, help = "name of docx")
    args = vars(ap.parse_args())
    return args["inputFile"]

def IOU(oldbox,newbox):
    (x1,y1,w1,h1) = oldbox
    (x2,y2,w2,h2) = newbox
    cx1 = x1 + w1/2
    cx2 = x2 + w2/2
    cy1 = y1 + h1/2
    cy2 = y2 + h2/2
    if cx1 >= x2 and cx1 <= x2+w2 and cy1>= y2 and cy1<= y2+h2:
        return True
    if cx2 >= x1 and cx2 <= x1+w1 and cy2>= y1 and cy2<= y1+h1:
        return True
    return False

def getTableCoordinate(image):
    """

    :param image:
    :return:
    listResult: x, y coordinates of layout 's bounding box
    listBigBox: x, y coordinates of table in image
    """
    # image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    kernel = np.ones((3, 3), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    (h1, w1) = image.shape
    blured = cv2.GaussianBlur(image, (11, 11), 0)
    canImage = cv2.Canny(blured, 100, 250)
    newimage = np.zeros_like(image)
    if imutils.is_cv2() or imutils.is_cv4():
        (conts, _) = cv2.findContours(canImage.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    elif imutils.is_cv3():
        (_, conts, _) = cv2.findContours(canImage.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    listBigBox = []
    listResult = []
    if len(conts) > 0:
        conts = contours.sort_contours(conts)[0]
        # conts = sorted(conts, key=lambda ctr: cv2.boundingRect(ctr)[0] + cv2.boundingRect(ctr)[1] * image.shape[1] )
        for i in range(len(conts)):
            (x, y, w, h) = cv2.boundingRect(conts[i])
            if w > 10 and h > 10 and w < 0.7 * w1:
                skip = False
                for temp in listResult:
                    for box in temp:
                        if IOU(box,(x,y,w,h)):
                            skip = True
                            break
                if skip == False:
                    over = False
                    for index,temp in enumerate(listResult):
                        if abs(temp[0][1]-y) <= 5:
                            listResult[index].append((x,y,w,h))
                            over = True
                    if over == False:
                        listResult.append([(x,y,w,h)])
                    # printImage(newimage)
            if w > 10 and h > 10 and w > 0.7 * w1:
                skip = False
                for box in listBigBox:
                    if IOU((x,y,w,h),box):
                        skip = True
                        break
                if skip == False:
                    listBigBox.append((x,y,w,h))
    ## sort
    for index,_ in enumerate(listResult):
        listResult[index] = sorted(listResult[index], key=lambda x: x[0])
    listResult = sorted(listResult,key=lambda x: x[0][1])
    listBigBox = sorted(listBigBox,key=lambda x: x[1])
    # for temp in listResult:
    #     for (x,y,w,h) in temp:
    #         cv2.rectangle(newimage, (x, y), (x + w, y + h), 255, 1)
    # for (x,y,w,h) in listBigBox:
    #     cv2.rectangle(newimage, (x, y), (x + w, y + h), 255, 1)
    # printImage(newimage)
    return listResult, listBigBox

def compare_table(item1, item2):
    # return (item1[2]-item2[2])/10
    if (item1[2] - item2[2]) // 10 > 0:  # return 1 means swap
        return 1
    elif (item1[2] - item2[2]) // 10 < 0:
        return -1
    else:
        return item1[1] - item2[1]


def retreiveTextFromTable(listResult,image):
    results = []
    for cnt in listResult:
        x, y, w, h = cnt
        crop = image[y:y + h, x:x + w]
        output_tesseract = pytesseract.image_to_string(crop,
                                                lang='vie')
        if output_tesseract == '':
                continue
        results.append(output_tesseract)
    return results                                        