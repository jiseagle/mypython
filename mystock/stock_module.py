# Program: Python Modules for Stock Price Notification
# get_setting(): get stock name, price setting.
# get_price(stockid): get real time stock price
# get_best(stockid): get best for buy or sell
# get_ifttt(v1,v2,v3): request ifttt to send message to LINE
# Author:Norman Chen
# -*- coding:utf-8 -*-

# import necesarry libaries
import twstock
import requests

def get_setting():
    res=[]        # create a empty list for reading and analyzing results.
    
    try:
        with open ('stock.txt', 'r', encoding='utf-8') as f: # open stock.txt by with method
            slist = f.readlines()                            # read data into a list called slist
            print('讀入:', slist)                             
            for lst in slist:                                # read each content in the list, and split by ','
                s = lst.split(',')
                res.append([s[0].strip(), float(s[1]), float(s[2])])  # write results to res[]
            
    except:
        print("讀入 stock.txt 錯誤")
    
    return res

def get_price(stockid):
    rt = twstock.realtime.get(stockid)
    if (rt['success']):
        return (rt['info']['code'], float(rt['realtime']['latest_trade_price']))
    
    else:
        return (False, False)

def get_best(stockid):
    stock = twstock.Stock(stockid)
    bp = twstock.BestFourPoint(stock).best_four_point()
    
    if(bp):
        return ('買進' if (bp[0]) else '賣出', bp[1])
    else:
        return(False, False)


def send_ifttt(v1, v2, v3):
    url = ('https://maker.ifttt.com/trigger/toline/with'+
           '/key/hZ9Txjltyh24_8m_f7KCaTkL-K8PrLC_WbWyjM548Dr'+
           '?value1='+str(v1) +'&value2='+str(v2)+'&value3='+str(v3))
    
    r = requests.get(url)
    if r.text[:5]== 'Congr':
        print('已傳送(' + str(v1) + ', '+ str(v2) + ', ' + str(v3) + ') 到Line')    
    else:
        print('傳送失敗')
    
    return r.text
