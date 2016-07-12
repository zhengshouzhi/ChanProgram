 # -*- coding: utf-8 -*-
from DataInter import *
import matplotlib.pyplot as plt
import datetime
from time import strftime, localtime
from GenProcess import *
from DataProcess import *
from StrProcess import *
from StrApplication import *
import numpy as np


if __name__=="__main__":
    Perf_Stat_2 = DataFrame([],index=['盈利','亏损'],columns =
                       ['0-5','5-10','10-15','15-20','20-30','30-50','50-100','>100','总次数'])
    Perf_Stat_2.loc['盈利'] = 0
    Perf_Stat_2.loc['亏损'] = 0
    Perf_Stat_2 = WinLoss_Stat(-0.12,Perf_Stat_2)

    print(Perf_Stat_2)

#     Price = Latest_Close('734508','D')
#     print(Price)
#    VolaList(0,700,'D')
#    MFITrendStat()
#    S_Trd_Data = Get_TrData_FromExc(FilePath='D:\Chan Program\SD510050.xlsx',ColIndex = 'Timestamp',Worksheet = '日线')
#    StockCode = 'sh'
#    AllCyclePro(StockCode)

#     stock_code_list = Sel_Stock_PB3BDFX()
#     Lv1Process('600221','5')  #明天接着测试
#     SellDate = get_Trday_of_day(1)
#     BuyDate = get_Trday_of_day(2)
#     Stock_Performance(SellDate,BuyDate)
#     FilePath = 'D:\Chan Data\Selected Stock\Date2016-01-21.xls'
#     Sel_Stock_All_Cycle(FilePath = FilePath)

#     stock_code_list = Get_LowStock()
#     print(stock_code_list)
#     enddate = get_Trday_of_day(0)
#     startdate = get_Trday_of_day(4)
#     print(startdate)
#     FilePath = 'D:\Chan Data\Selected Stock\Date'+startdate+'.xls'
#     Sel_Stock_Perf(FilePath,enddate,startdate)
#     stock_code_list = Sel_StockPB3BDFX(5)
#     SelStockPerf(n=5)








