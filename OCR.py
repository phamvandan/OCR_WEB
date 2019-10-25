import os
from utils.supportFunc import preprocessFile, processPdfFile
from os import walk

projectPath = '/home/trandat/project/OCR_WEB/'


processPdfFile(projectPath+'static/data/', projectPath+'static/OCR_origin/', projectPath+'static/OCR_edited/' )