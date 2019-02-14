# photo parser
# Author:Norman Chen
# -*- coding:utf-8 -*-
# import necessary library
import requests
from bs4 import BeautifulSoup

def getPhotolist(photo_name, download_num):
    page = 1                      # initial page = 1
    photo_list = []               # create a empty phot list
    
    while True:
        url = 'https://pixabay.com/zh/photos/'+ str(photo_name) + '/?&pagi=' + str(page)
        
        html = requests.get(url)  # GET request from url
        html.encoding = 'utf-8'   # set encoding as utf-8
        bs = BeautifulSoup(html.text, 'lxml')    # Analyze Webpage
        photo_item = bs.find_all('div', {'class':'item'})
        
        if len(photo_item) == 0:   # if not find item, then return None
            return None
        
        for i in range(len(photo_item)):
            photo = photo_item[i].find('img')['src']
            
            if photo in photo_list:
                return photo_list
            elif photo == '/static/img/blank.gif':
                photo = photo_item[i].find('img')['data-lazy']
            
            photo_list.append(photo)
            
            if len(photo_list) >= download_num:
                return photo_list
        
        page=page+1
        