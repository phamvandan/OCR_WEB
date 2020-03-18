# eDOCUMENT

In this project, we build a demo web base on Flask for eDocument with some features:  
- OCR for pdf,image files with tesseract
- Convert from pdf,image to docx file
- Save and Search documents with Elastic Search  

###Project build base on Ubuntu 18.04 LTS

## Some require libraries and how to install

1. Tesseract:  

    - sudo apt install tesseract-ocr 
    - sudo apt install tesseract-ocr-<language options>  
       Example for Vietnamese : sudo apt install tesseract-ocr-vie  
  or for all language : sudo apt install tesseract-ocr-all  
  
2. ElasticSearch :  
    - Install ElasticSearch :[Vietnamese Tutorial](https://stackjava.com/elasticsearch/huong-dan-cai-dat-elasticsearch-tren-ubuntu-16-04.html)
or [ElasticSearch install guide](https://www.elastic.co/guide/en/elasticsearch/reference/current/install-elasticsearch.html)  
    - After install <b>make sure elastic search run on port 9200</b>

3. Install some requirement packages :  
    - We recommend use a virtual environment  
    - Then : pip install -r requirements  
    
# Run demo
* Down load or clone this project : git clone https://github.com/tranmanhdat/OCR_WEB
* cd OCR_WEB
* python demo.py
* then go a browser (chrome, firefox..), go to http://localhost:5000/