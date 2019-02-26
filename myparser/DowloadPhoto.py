# photo parser main progaom
# Author:Norman Chen
# -*- coding:utf-8 -*-
# import necessary library
import photo_module as pm
import PicDownload as PD
import os

while True:
    
    photo_name, download_num, folder_name = pm.create_folder()
    
    photo_list = pm.getPhotolist(photo_name, download_num)
    
    if photo_list == None:
        print("[INFO] ===> There is nothing to be found, please correct keyword .....")
        os.rmdir(folder_name + os.sep + photo_name)                                    # remove the wrong folder
    
    elif photo_name is False:                                                          # there is the same folder name as keyword
        print("[INFO] ===> There is same folder name, please input photo folder name again ....")
               
    else:
        if len(photo_list) < download_num:
            print("[INFO] ===> Only can find", len(photo_list), "pictures")
        
        else:
            print("[INFO] ===> Successfully getting connections of all pictures.")
        
        break

print("[INFO] ===> Start to download pictures.......")

pm.get_photobythread(folder_name, photo_name, photo_list)

print("[INFO] ===> Totally, we get {} pictures.......".format(len(photo_list)))