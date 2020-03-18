import flask
from flask import Flask, flash, request, redirect, render_template, url_for
import urllib.request
from werkzeug.utils import secure_filename
import os
from utils.supportFunc import preprocessFile
from utils.detai import ocr_file
import requests

text_ocr = ocr_file("./testdata/15.pdf", True, True, True, False)

# print(text_ocr)
