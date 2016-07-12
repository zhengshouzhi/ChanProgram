# -*- coding: utf-8 -*-
from GenProcess import *
from DataInter import *
import pandas as pd
from pandas import ExcelWriter
from StrApplication import *
import types
#有某些数据缺陷需要解决
def Sel_Stock_Perf(FilePath='FilePath',SellDate = 'SellDate',BuyDate = 'BuyDate'):
    Sel_Stock_list = pd.read_excel(io=FilePath,sheetname='StockList')
    list = Sel_Stock_list['stockcode']
    Buy_Price_List = []
    Sell_Price_List = []
    RisePercent_List = []
    for stockcode in list:

        stockcode = codeType(stockcode)
        Trd_Data = Get_TrData_FromTs(StockCode=stockcode,AnaCycle='D',startDate=BuyDate,endDate=SellDate)

        totalrows = len(Trd_Data)
        print(totalrows)
        #此处的数据可能存在缺陷，仍需解决
        if(totalrows >= 2):
            BuyPrice = Trd_Data.loc[0,'close']
            SellPrice = Trd_Data.loc[totalrows-1,'close']
            RisePercentage = (SellPrice-BuyPrice)/BuyPrice
        else:
            BuyPrice = '无'
            SellPrice = '无'
            RisePercentage = '无'

        Buy_Price_List.append(BuyPrice)
        Sell_Price_List.append(SellPrice)
        RisePercent_List.append(RisePercentage)
    totalcols = len(Sel_Stock_list.columns)
    Sel_Stock_list.insert(totalcols,'BuyPrice',value = Buy_Price_List)
    totalcols = totalcols + 1
    Sel_Stock_list.insert(totalcols,'SellPrice',value = Sell_Price_List)
    totalcols = totalcols + 1
    Sel_Stock_list.insert(totalcols,'Rise',value = RisePercent_List)
    writer = ExcelWriter(FilePath)
    Sel_Stock_list.to_excel(writer,'StockList')
    writer.save()
#统计选出股票的市场表现，参数Date为日期
def Stock_Performance (SellDate = 'SellDate',BuyDate = 'BuyDate'):
     FilePath = 'D:\Chan Data\Selected Stock\Str1\Date'+BuyDate +'.xls'
     Sel_Stock_Perf(FilePath,SellDate,BuyDate)

def SelStockPerf(n=5):
    i = 1
    SellDate = get_Trday_of_day(0)
    while(i<=n):
        BuyDate =get_Trday_of_day(i)
        Stock_Performance(SellDate,BuyDate)
        i = i+1

#对于输入的路径下的股票列表中的数据进行全周期处理。
def Sel_Stock_All_Cycle(FilePath='FilePath'):
    Sel_Stock_list = pd.read_excel(io=FilePath,sheetname='PanBei')
    list = Sel_Stock_list['stockcode']
    for stockcode in list:
        stockcode = str(stockcode)
        stockcode = stockcode.zfill(6)
        AllCyclePro(stockcode)

