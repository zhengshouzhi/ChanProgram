 # -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import datetime
import time
from matplotlib.dates import AutoDateLocator,DateFormatter
from pandas import  DataFrame, Series

def StrToTime(x = 'x'):
    totalrows = len(x)
    irows = 0
    while (irows < totalrows - 1):
        t = x[irows]
    #用数据的长度判断是年月日还是年月日时分秒格式，格式为来自Excel时，可能存在问题。
        if(len(t) == 19):
            trdDay = time.strptime(t, "%Y-%m-%d %H:%M:%S")
        elif(len(t) == 10):
            trdDay = time.strptime(t, "%Y-%m-%d")
        trdDay = datetime.datetime(* trdDay[:6])
        x[irows] = trdDay
        irows = irows + 1
    return x

#给出存储笔数据的表格，打印笔图
def BiPlot(Bi_Data = 'Bi_Data'):
    x = Series(Bi_Data['TrDays'])
    length = len(x)
    index = length
    x[length] = 0
    while(index > 0):
        x[index] = x[index-1]
        index = index - 1
    x[0] = 0
    index = 1
    while (index <= length):
        x[index] = x[index-1]+x[index]
        index = index + 1
    y = Series(Bi_Data['startPrice'])
    totalrows = len(y)
#    x[totalrows] = Bi_Data.loc[totalrows-1,'endDate']
    y[totalrows] = Bi_Data.loc[totalrows-1,'endPrice']
#    x = StrToTime(x)
    plt.xlabel(u'Date')
    plt.ylabel(u'Price')
    plt.grid(True)
#    autodates = AutoDateLocator()
#    yearsFmt = DateFormatter('%Y-%m-%d')
#    fig,ax = plt.subplots()
#    ax.xaxis.set_major_locator(autodates)
#    ax.xaxis.set_major_formatter(yearsFmt)
    plt.plot(x, y, 'black')
    for xy in zip(x,y):
        plt.annotate(xy[1], xy=xy)
    plt.show()
#    fig.autofmt_xdate()

