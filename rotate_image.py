import os
from random import randint, seed
import numpy as np
import cv2
from utils.skew_process.rotation import rotateAndScale

# path = 'data/no_table/image/'
# path_save = 'data/no_table/image_skew/'
path = 'data/table/image/'
path_save = 'data/table/image_skew/'
list_subfolders_with_paths = [f.path for f in os.scandir(path) if f.is_dir()]
id = 0
for subfolder in list_subfolders_with_paths:
  print(subfolder)
  path_to_subfolder = os.path.join(path_save, subfolder.split('/')[-1])
  if not os.path.exists(path_to_subfolder):
    os.makedirs(path_to_subfolder)
  images = os.listdir(subfolder)
  print(images)
  for image in images:
      path_to_origin = os.path.join(subfolder, image)
      path_to_save = os.path.join(path_to_subfolder, image)
      img = cv2.imread(path_to_origin)
      if id<20:
        id = id+1
        angle = randint(0,360)
        img = rotateAndScale(img, angle)
      cv2.imwrite(path_to_save, img)
