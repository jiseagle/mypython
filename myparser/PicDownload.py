# Download Picture from internet
# Author:Norman Chen
# -*- coding:utf-8 -*-

# import necesarry libaries
import requests

def picDownload(url, path):
    pic = requests.get(url)
    path = path + url[url.rfind('.'):]       # url.rfind('.') return index of '.', and url[url.rfind('.'):] return the ".xxx" by sliding.
    
    with open(path, "wb") as f:              # write content, use with open() which will close file automatically.
        f.write(pic.content)

