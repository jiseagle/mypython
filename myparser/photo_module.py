# photo parser module
# Author:Norman Chen
# -*- coding:utf-8 -*-
# import necessary library
import requests
from bs4 import BeautifulSoup
import os
import threading
import PicDownload as PD

def get_photobythread(folder_name, photo_name, photo_list):
    download_num = len(photo_list)             # set total download number is the same as the length of photo_list
    Q = int(download_num/100)
    R = download_num % 100
    
    for i in range(Q):
        threads = []
        for j in range(100):
            threads.append(threading.Thread(target = PD.picDownload, args = (photo_list[i*100+j], folder_name + os.sep +
                                                                           photo_name + os.sep + str(i*100+j+1))))
            threads[j].start()
        for j in threads:
            j.join()
        print("[INFO] ===> Download Progress is ", int((i+1)*100/download_num*100), '%')
    
    threads = []
    
    for i in range(R):
        threads.append(threading.Thread(target = PD.picDownload, args = (photo_list[Q*100+i], folder_name + os.sep +
                                                                           photo_name + os.sep + str(Q*100+i+1))))
        threads[i].start()
    for i in threads:
        i.join()
    print("[INFO] ===> Download is 100% finished")
    

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


def create_folder():
    
    photo_name = input("[INFO] ===> Please insert the name of photo you want search: ")
    
    while True:
        download_num = input("[INFO] ===> Please insert the total numbers of photos you want to download: ")
        try:
            download_num = int(download_num)
            if download_num > 0:
                break
            
            else:
                print("[INFO] ===> Please input positive integer for how many numbers of pictures you want to download ...... \n")

        except ValueError:
            print("[INFO] ===> Please input positive integer for how many numbers of pictures you want to download ...... \n")   

    folder_name = input("[INFO] ===> Please input folder name: ")
    
    if os.path.exists(folder_name) is False:
        os.mkdir(folder_name)
        os.mkdir(folder_name + os.sep + photo_name)
        print("[INFO] ==> Create new folder: {} .....".format(os.sep + folder_name + os.sep + photo_name))
        return (photo_name, download_num, folder_name)
        
    elif os.path.exists(folder_name) is True:
        if os.path.exists( folder_name + os.sep+ photo_name) is True:
            print("[INFO] ==> the {} folder is exist ....".format(os.sep + folder_name + os.sep + photo_name))
            new_folder = input("[INFO] ===> Do you want to continou (Y/n)? ")
            if new_folder == "Y" or new_folder == "y":
                return (photo_name, download_num, folder_name)
            else:
                return (False, download_num, False)
        else:
            os.mkdir(folder_name + os.sep + photo_name)
            print("[INFO] ==> Create new folder: {} .....".format(os.sep + folder_name + os.sep + photo_name))
            return (photo_name, download_num, folder_name)

    
    