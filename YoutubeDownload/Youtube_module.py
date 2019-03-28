# Youtube Download by Pytube
# Author:Norman Chen
# -*- coding:utf-8 -*-
# import necessary library

from bs4 import BeautifulSoup
import requests
from pytube import YouTube
import threading
import tkinter as tk
import os
import subprocess

lock = threading.Lock()

def start_download(url, listBox):
    yt = YouTube(url)
    title = yt.title           #影片名稱
    
    lock.acquire()
    num = listBox.size()
    listBox.insert(tk.END, f'下載中: {num:02d}:{title}')
    lock.release()
    
    if os.path.exists(os.getcwd()+os.sep+'download'):
        yt.streams.first().download(os.getcwd()+os.sep+'download')  #開始下載影片
    
    else:
        os.mkdir('download')
        yt.streams.first().download(os.getcwd()+os.sep+'download')  #開始下載影片
    
    lock.acquire()
    listBox.delete(num)
    listBox.insert(num, f'下載完成: {num:02d}:{title}')
    lock.release()

def start_downloadm(url, listBox):
    yt = YouTube(url)
    title = yt.title           #影片名稱
    
    name = str()               # remove '.', '/' from file name.
    for i in title:
        if i == '.':
            name = name
        elif i == '/':
            name = name
        elif i ==':':
            name=name
        else:
            name = name + i
    
    name1  = name + ".mp4"
    name2 = name + ".mp3"
    
    lock.acquire()
    num = listBox.size()
    listBox.insert(tk.END, f'下載中: {num:02d}:{title}')
    lock.release()
    
    if os.path.exists(os.getcwd()+os.sep+'download'):
        yt.streams.first().download(output_path=os.getcwd()+os.sep+'download', filename=title)  #開始下載影片
    
    else:
        os.mkdir('download')
        yt.streams.first().download(output_path=os.getcwd()+os.sep+'download', filename=title)  #開始下載影片
    
    # Use ffmpeg transfer mp4 to mp3   
    subprocess.call(['ffmpeg', '-i', os.path.join(os.getcwd()+os.sep+'download', name1),
                    os.path.join(os.getcwd()+os.sep+'download', name2)])
    
    os.remove(os.getcwd()+os.sep+'download'+os.sep+name1)  #remove mp4 file
    
    lock.acquire()

    listBox.delete(num)
    listBox.insert(num, f'下載完成: {num:02d}:{title}')
    lock.release()

def get_urls(url):
    urls = []
    title1 = []
    if '&list=' not in url:                         # if '&list' is not in url, 表示是單一影片
        return urls
    
    response = requests.get(url)                    # 發送get請求

    if response.status_code != 200:                 # 如果網站請求失敗(code!=200), 輸出"網址請求失敗"
        print("網址請求失敗!!")
        return False
    
    # ----- 請求成功，開始解析網頁 -------
    bs = BeautifulSoup(response.text, 'lxml')
    a_list = bs.find_all('a')
    web = 'https://www.youtube.com/'
    
    # ----- 獲取各個影片的網址 -----------
    for a in a_list:
        href = a.get('href')
        url1 = web + href
        if ('&index=' in url1) and (url1 not in urls):
            urls.append(url1)
    
    """# ----- 取得各個影片的title ----------- 
    title_list = bs.find_all('h4', {'class':'yt-ui-ellipsis yt-ui-ellipsis-2'})
    
    for i in title_list:
        title = i.get_text().strip()
        if title not in title1:
            title1.append(title)"""
            
    return urls
       