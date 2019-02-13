# Program: Main Program for Stock Price Notification
# Author:Norman Chen
# -*- coding:utf-8 -*-

# import necessary modules
import stock_module as stm
import time

stockList = stm.get_setting()    # get setting data
cnt = len(stockList)             # count how many stock

log1 = []
log2 = []

for i in range(cnt):
    log1.append(' ')
    log2.append(' ')

check_cnt = 20                  # check time (20 times * 3 mins = 60mins)

while True:
    for i in range(cnt):
        stockid, lowPrice, highPrice = stockList[i]
        name, rtPrice = stm.get_price(stockid)
        print("檢查:", name, " |即時股價:", rtPrice, " |股價區間(低~高):", lowPrice, highPrice)

        if (rtPrice <= lowPrice):
            if (log1[i] != "買進"):
                stm.send_ifttt(name, str(rtPrice), "買進 (股價低於" + str(lowPrice) +")")
                log1[i] = "買進"
        elif (rtPrice >= highPrice):
            if (log1[i] != "賣出"):
                stm.send_ifttt(name, str(rtPrice), "賣出 (股價高於"+ str(highPrice) + ")")
                log1[i] = "賣出"
        act, why = stm.get_best(stockid)
        
        if(why):
            if (log2[i] != why):
                stm.send_ifttt(name, rtPrice, act + "(" + why + ")")
                log2[i] = why
    
    print("-------------------------------------------------")
    check_cnt -= 1
    if check_cnt == 0:
        break
    time.sleep(180)
        