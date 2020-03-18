# OCR_WEB
In this project, we build a demo web base on Flask for eDocument with some features:  
- OCR for pdf file
- Convert to docx file
- Searching documents with Elastic Search

# Some require libraries and how to install

## tesseract and pytesseract  
sudo apt install tesseract-ocr 
-- need sudo apt install tesseract-ocr-<language options> example vie for vietnamese,use all for get all language
sudo apt install libtesseract-dev  
sudo pip3 install pytesseract  
sudo apt-get install python-pypdf2  
sudo pip3 install imutils pdf2image python-docx PyPDF2
sudo pip3 install matplotlib
sudo pip3 install  numpy scipy matplotlib ipython jupyter pandas sympy nose poppler-utils

# install ElasticSearch : 
https://stackjava.com/elasticsearch/huong-dan-cai-dat-elasticsearch-tren-ubuntu-16-04.html  
make sure elastic search run on port 9200

oke done