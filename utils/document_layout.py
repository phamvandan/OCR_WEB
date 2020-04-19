import enum

import cv2
import numpy as np
import matplotlib.pyplot as plt


def display_plot(x_val, y_val):
    mean = np.mean(np.array(y_val))
    plt.plot(x_val, y_val)
    plt.ylabel('y')
    plt.xlabel('x')
    plt.axhline(y=mean, color='r')
    plt.axhline(y=mean / 4, color='b')
    plt.show()


def iou(oldbox, newbox):
    (x1, y1, w1, h1) = oldbox
    (x2, y2, w2, h2) = newbox
    cx1 = x1 + w1 / 2
    cx2 = x2 + w2 / 2
    cy1 = y1 + h1 / 2
    cy2 = y2 + h2 / 2
    if cx1 >= x2 and cx1 <= x2 + w2 and cy1 >= y2 and cy1 <= y2 + h2:
        return True
    if cx2 >= x1 and cx2 <= x1 + w1 and cy2 >= y1 and cy2 <= y1 + h1:
        return True
    return False


def determine_threshold(x_val, mean, devide=4):
    start_index = -1
    end_index = -1
    arr = []
    first = True
    # print("mean thresh",mean/devide)
    for i in range(len(x_val)):
        if x_val[i] < mean / devide:
            if first:
                start_index = i
                end_index = i
                first = False
                continue
            if start_index == -1:
                start_index = i
            end_index = i
        else:
            # if start_index!=-1 and start_index!=end_index:
            if end_index - start_index > 5:
                arr.append([start_index, end_index - start_index])
            start_index = -1
            end_index = start_index
    arr = sorted(arr, key=lambda x: x[1], reverse=True)
    if len(arr) > 3:
        arr = arr[:3]
    arr = sorted(arr, key=lambda x: x[0], reverse=False)
    # print(arr)
    return arr


def do_split(box, arr, split_thresh=1):
    (x, y, w, h) = box
    split_indexes = []
    temp = x
    for index, width in arr:
        if width > split_thresh * h:
            split_indexes.append((x, x + index))
            x = x + index + width
    split_indexes.append((x, temp + w))
    boxes = []
    for start, end in split_indexes:
        newbox = (start, y, end - start, h)
        boxes.append(newbox)
    return boxes


## split using opencv
def split_using_cv(box, image, show=False, scale=2, split_thresh=1):
    (x, y, w, h) = box
    # image = image[max(0, y - 1):y + h + 1, x:x + w].copy()
    image = image[y + h // 5:y + 4 * h // 5, x:x + w]
    # temp = image.copy()
    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    kernel = np.ones((5, 5), np.uint8)
    image = cv2.erode(image, kernel, iterations=3)
    image = cv2.dilate(image, kernel, iterations=1)
    image = ~image
    image = imutils.resize(image, width=w // scale)
    # printImage(image)
    height, width = image.shape[:2]
    # print(height,width)
    x_val = []
    y_val = []
    for i in range(width):
        sum = 0
        for j in range(height):
            sum = sum + image[j][i]
        x_val.append(sum)
        y_val.append(i)
    arr = determine_threshold(x_val, mean=np.mean(np.array(x_val)))
    for index, _ in enumerate(arr):
        arr[index][0] = arr[index][0] * scale
        arr[index][1] = arr[index][1] * scale
    boxes = do_split(box, arr, split_thresh=split_thresh)
    if show:
        print(arr)
        cv2.imshow("crop", image)
        display_plot(y_val, x_val)
        cv2.waitKey(1)
    return boxes


## region IOU
def region_iou(original_box, box, scale=0.9):
    (ori_x, ori_y, ori_w, ori_h) = original_box
    ori_center_x = ori_x + ori_w / 2
    ori_center_y = ori_y + ori_h
    (x, y, w, h) = box
    center_x = x + w / 2
    center_y = y
    if (center_x > ori_x and center_x < ori_x + ori_w) or (ori_center_x > x and ori_center_x < x + w) or (
            x > ori_x and x < ori_x + ori_w) or (ori_x > x and ori_x < x + w):
        if abs(center_x - ori_center_x) <= min(ori_h, h) * 0.5 and abs(center_y - ori_center_y) <= min(ori_h,h)*scale:  # (ori_h + h)*scale:
            return True
        if abs(center_y - ori_center_y) <= min(ori_h, h)*scale:  # (ori_h + h)*scale:
            # indent
            if x - ori_x <= 0:
                return True
            if x - ori_x > 0 and abs(x - ori_x) < min(ori_h, h):
                return True
    return False


## line IOU
def line_iou(original_box, box):
    (ori_x, ori_y, ori_w, ori_h) = original_box
    ori_centery = ori_y + ori_h / 2
    (x, y, w, h) = box
    centery = y + h / 2
    if ori_centery > y and ori_centery < (y + h):
        return True
    if centery > ori_y and centery < (ori_y + ori_h):
        return True
    return False


def box_iou(large_box, small_box):
    (x, y, w, h) = large_box
    (a, b, c, d) = small_box
    if x <= a and y <= b and (x + w) >= (a + c) and (y + h) >= (b + d):
        return True
    return False


def add_box_info(original_box, box, box_info):
    # if line_iou(original_box,box):
    #     box_info.append(1)
    #     return 0
    if region_iou(original_box, box):
        box_info.append(1)
        return 0
    box_info.append(0)


## box_info box,1-line,2-region,0 alone
## region grouping
def region_grouping(boxes):
    boxes_fully = []
    if len(boxes)>2:
        stop = len(boxes) - 2
        for index, box in enumerate(boxes):
            box_info = []
            if index == stop:
                add_box_info(box, boxes[index + 1], box_info)
                box_info.append(0)
                boxes_fully.append(box_info)
                boxes_fully.append((0, 0))
                break
            add_box_info(box, boxes[index + 1], box_info)
            add_box_info(box, boxes[index + 2], box_info)
            boxes_fully.append(box_info)
    else:
        boxes_fully.append((0, 0))
    return boxes_fully


def merge_region(region):
    # print(region)
    merged = [region[0][0], region[0][1], region[0][2], region[0][3]]
    for index, box in enumerate(region):
        if index == 0:
            continue
        (x, y, w, h) = box
        merged[2] = max(x + w, merged[0] + merged[2]) - min(merged[0], x)
        merged[0] = min(merged[0], x)
        merged[3] = h + y - merged[1]
    return merged


def layout_document(box_info, boxes):
    layout = []
    mark = [0] * len(boxes)
    merged = None
    for index, box in enumerate(boxes):
        if mark[index] == 0:
            if merged is not None and box_iou(merged, box):
                mark[index] = 1
                continue
            regions = []
            regions.append(box)
            mark[index] = 1
            while not (box_info[index][0] == 0 and box_info[index][1] == 0):
                if box_info[index][0] == 1:
                    regions.append(boxes[index + 1])
                    index = index + 1
                    mark[index] = 1
                elif box_info[index][1] == 1:
                    regions.append(boxes[index + 2])
                    index = index + 2
                    mark[index] = 1
            merged = merge_region(regions)
            merged = tuple(merged)
            # merged at 0 position
            regions.insert(0, merged)
            layout.append(regions)
    return layout


## xu ly truong hop chua group het
def append_and_group(region, line):
    (ori_x, ori_y, ori_w, ori_h) = region[0]
    ori_center_x = ori_x + ori_w / 2
    for index, old_region in enumerate(line):
        (x, y, w, h) = old_region[0]
        center_x = x + w / 2
        if (center_x > ori_x and center_x < ori_x + ori_w) or (ori_center_x > x and ori_center_x < x + w):
            merged = merge_region([old_region[0], region[0]])
            line[index][0] = tuple(merged)
            for box in region[1:]:
                line[index].append(box)
            return True
    line.append(region)
    return False


def add_lines(layout):
    lines = []
    if len(layout)==0:
        return lines
    lines.append([layout[0]])
    for region in layout[1:]:
        skip = False
        for index, item in enumerate(lines):
            for region_item in item:
                if line_iou(region_item[0], region[0]):
                    append_and_group(region, lines[index])
                    skip = True
                    break
        if skip:
            continue
        lines.append([region])
    for index, line in enumerate(lines):
        if len(line) > 1:
            lines[index].sort(key=lambda x: x[0])
    return lines


def layout_processing(boxes, img, debug=False):
    newboxes = []
    for box in boxes:
        boxs = split_using_cv(box, img, split_thresh=1.5)
        for temp in boxs:
            if temp[2]<5 or temp[3]<5:
                continue
            newboxes.append(temp)
    print("newboxes ",newboxes,"\n\n")
    boxes_info = region_grouping(newboxes)
    print("boxes_info",boxes_info)
    # for index,box in enumerate(newboxes):
    #     (x, y, w, h) = box
    #     cv2.putText(img,str(boxes_info[index]),(x,y),cv2.FONT_HERSHEY_SIMPLEX,1,color=(0,0,255),thickness=2)
    #     cv2.rectangle(img, (x, y), (x + w, y + h), 255, 1)
    # printImage(img)
    layout = layout_document(boxes_info, newboxes)
    lines = add_lines(layout)
    if debug:
        for line in lines:
            for region in line:
                (x, y, w, h) = region[0]
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        printImage(img)
    return lines


import imutils


def printImage(image, name="ok"):
    image = imutils.resize(image, width=800)
    cv2.imshow(name, image)
    cv2.waitKey(0)
