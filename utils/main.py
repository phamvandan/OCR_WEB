import numpy as np
import pytesseract
from pytesseract import Output

from utils.document_layout import iou
from utils.to_word import to_word


def entry_dla(img,document, rule_base, auto_correct):
    d = pytesseract.image_to_data(img, output_type=Output.DICT)
    (height, width) = img.shape[:2]
    n_boxes = len(d['text'])
    boxes = []
    for i in range(n_boxes):
        if int(d['conf'][i]) < 0:
            # print(int(d['conf'][i]))
            (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
            newbox = (x, y, w, h)
            if w == width or h == height or w < h / 2 or w<10 or h <10:
                continue
            if len(boxes) > 0 and iou(boxes[-1], newbox):
                # bigBoxes.append(boxes[-1])
                del boxes[-1]
            boxes.append(newbox)
    arr = np.array([box[3] for box in boxes])
    mean = np.mean(arr)
    dec = 0
    temp = boxes.copy()
    limit = 30
    for index, box in enumerate(temp):
        if box[3] > 2 * mean or box[0]<=limit or box[1]<=limit or box[2]>=width-limit or box[3]>=height-limit:
            del boxes[index - dec]
            dec = dec + 1
    all_text = to_word(boxes, img,document,rule_base,auto_correct)
    return all_text

# import time
# if __name__ == "__main__":
#     filenames = glob.glob("./temp/*")
#     for filename in filenames:
#         if sys.argv[1] not in filename:
#             continue
#         img = cv2.imread(filename)
#         entry_dla(img)