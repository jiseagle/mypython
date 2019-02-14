# photo parser main progaom
# Author:Norman Chen
# -*- coding:utf-8 -*-
# import necessary library
import photo_module as pm
import PicDownload as PD

while True:
    photo_name = input("[INFO] ===> Please insert the name of photo you want search: ")
    
    download_num = int(input("[INFO] ===> Please insert the total numbers of photos you want to download: "))
    
    photo_list = pm.getPhotolist(photo_name, download_num)
    
    if photo_list == None:
        print("[INFO] ===> It cannot find the photos, please change the keyword")
    
    else:
        if len(photo_list) < download_num:
            print("[INFO] ===> Only can find", len(photo_list), "pictures")
        
        else:
            print("[INFO] ===> Successfully getting connections of all pictures.")
            break
    

print("[INFO] ===> Start to download pictures.......")

for i in range(len(photo_list)):
    PD.picDownload(photo_list[i], str(i+1))
    print("[INFO] ===> Picture number {0} download finished.......".format(i+1))

print("[INFO] ===> Dowload Process is finished.......")