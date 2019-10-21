import flask
from flask import Flask, flash, request, redirect, render_template, url_for
import urllib.request
from werkzeug.utils import secure_filename
import os
from utils.supportFunc import preprocessFile
import requests

text_ocr = preprocessFile("image", "/home/trandat/project/OCR_WEB/test" , "test.txt" )