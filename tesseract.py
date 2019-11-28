import os
from utils.supportFunc import preprocessFile, processPdfFile, tesseractPdf
from os import walk

projectPath = '/home/dat_tran/project/OCR_WEB/'

tesseractPdf(projectPath+'static/data/', projectPath+'static/tesseract/')