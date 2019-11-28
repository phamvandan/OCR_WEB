import flask
from flask import Flask, flash, request, redirect, render_template, url_for
import urllib.request
from werkzeug.utils import secure_filename
import os
from utils.supportFunc import preprocessFile
from utils.detai import ocrFile
import requests

text_ocr = ocrFile("/home/trandat/project/OCR_WEB/59.pdf",True,True,True,True,False)

print(text_ocr)