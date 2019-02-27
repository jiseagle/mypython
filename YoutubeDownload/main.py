# Youtube Donwloader
# Author:Norman Chen
# -*- coding:utf-8 -*-
# import necessary library

import tkinter as tk
from tkinter import messagebox
import Youtube_module as m
from pytube import YouTube
import threading

def click_func():
    url = yt_url.get()
    
    try:
        YouTube(url)
    except:
        messagebox.showerror('錯誤', 'pytube 不支援此影片或是網址錯誤!!')
    
    urls, titles = m.get_urls(url)
    
    if urls and messagebox.askyesno('確認方塊', '是否下載清單內所有影片?? (選擇[否], 則下載目前單一影片 )'):
        # ---- 開始執行下載 -------
        print("[INFO] ===> 開始下載......")
        
        for u in urls:
            threading.Thread(target=m.start_download, args=(u, listbox)).start()
    
    else:                                          # 下載單一影片
        yt = YouTube(url)
        if messagebox.askyesno("確認方塊", f'是否下載 {yt.title} 影片？'):
            print(f'[INFO] ===> 開始下載 {yt.title} 影片')
            threading.Thread(target=m.start_download, args=(url, listbox)).start()
        
        else:
            print(f"[INFO] ===> 取消下載 {yt.title} 影片")
    

# ------------ 主視窗 -----------------
window = tk.Tk()
window.geometry('640x480')
window.title('Youtube 急速下載器')

# ------------ Frame1:上方輸入網址區域 ----------------
frame1 = tk.Frame(window, bg = '#008899', width = 640, height = 120)  # 建立frame-1
frame1.pack()

# ------------ Label in Frame1:請輸入YouTube網址 -----
lb1 = tk.Label(frame1, bg='#008899', fg='black',text = '請輸入YouTube網址', font=('細明體', 12))
lb1.place(rely=0.2, relx=0.5, anchor ='center')

# ------------ Entry in Frame1 ----------------------
yt_url = tk.StringVar()
entry1 = tk.Entry(frame1, textvariable = yt_url, width=50, font=('細明體', 12))
entry1.place(rely=0.5, relx=0.5, anchor = 'center')

# ------------ Button: 下載影片 ---------------------
btn = tk.Button(frame1, text='下載影片', command = click_func, bg='#FFD700', fg='black', font=('細明體', 12))
btn.place(rely=0.5, relx=0.9, anchor='center')

# ------------ Frame2:下方顯示下載狀態區域 -----------
frame2 = tk.Frame(window, bg = 'gray', width = 640, height = 480-120)
frame2.pack()

# ------------ Label in Frame2: 下載狀態 ------------
lb2 =tk.Label(frame2, bg = 'gray', fg='black', text='下載資訊', font=('新細明體', 10))
lb2.place(rely=0.1, relx=0.5, anchor='center')

# ----------- ListBox in Frame2 ---------------------
listbox = tk.Listbox(frame2, width = 75, height = 16, font=('細明體', 10))
listbox.place(rely = 0.55, relx = 0.5, anchor='center')

# ----------- Scrollbar in ListBox ------------------
scrollbar = tk.Scrollbar(frame2)
scrollbar.place(rely=0.55, relx = 0.96, anchor='center', relheight=0.765)

# ----------- ListBox 與 Scrollbar的連結 ------------
listbox.config(yscrollcommand = scrollbar.set)
scrollbar.config(command = listbox.yview)

# ------------ 啟動主視窗 -------------
window.mainloop()