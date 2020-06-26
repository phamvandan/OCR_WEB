# eDOCUMENT

In this project, we build a demo web base on Flask for eDocument with some features:  
- OCR for pdf,image files with tesseract
- Convert from pdf,image to docx file  

### OCR_API build base on Windows 10

## Some require libraries and how to install

1. Tesseract:  
    install tesseract (	tesseract-ocr-setup-4.0.0dev-20161129.exe) for windows
    [tesseract](https://digi.bib.uni-mannheim.de/tesseract/)
    Remember get language when install

2. Install some requirement packages :  
    - We recommend use a virtual environment  with python 3.7
    - Then : pip install -r requirements  
    - install propper for windows:
        - download propper : https://poppler.freedesktop.org/poppler-0.89.0.tar.xz
        - extract and put it into C:\ProgramFile
        - add propper\bin to enviroment
# Run demo
* Down load or clone this project : git clone https://github.com/tranmanhdat/OCR_WEB
* checkout to deployt_API
* python demo.py
* then go a browser (chrome, firefox..), go to http://localhost:5000/