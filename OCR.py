import os
from utils.detai import preprocessFile,processPdfFile
from os import walk


projectPath = '/home/dat_tran/project/OCR_WEB/'


processPdfFile(projectPath+'static/data/', projectPath+'static/OCR_origin/', projectPath+'static/OCR_edited/', True, True, True, False )
