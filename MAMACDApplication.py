# -*- coding: utf-8 -*-
from DataProcess import *
from DataInter import *
from DataPlot import *
import datetime
from GenProcess import *
import pandas as pd
from StrProcess import *
from MAMACDProcess import *
from pandas import ExcelWriter
from MAMACDPerf import *

#在给定股票列有中，选出给定周期级别，在给定时间（如当天）突破特定均线的股票,属于选股程序,接着完成
def Sel_Stock_Over_Avg(FilePath =''):
    CodePath = FilePath + '\\'+ 'StockBelow'+'.xls'
    FilePath1 = FilePath
    FilePath2 = FilePath1 + '\\' + 'HisData'
    stockcodelist = Get_TrdData_FromExcel(CodePath,'BelowList')
    totalrows = len(stockcodelist)   #股票数量
    irows = 0
    dfup = DataFrame([],columns=['stockcode','名称'])
    dfdown = DataFrame([],columns=['stockcode','名称'])
    FilePathUp = FilePath1 + '\\'+ 'curup.xls'
    FilePathBelow = FilePath1 + '\\'+ 'below.xls'
    while(irows < totalrows):
        stockcode = stockcodelist.loc[irows,'stockcode']
        stockcode = codeType(stockcode)
        FilePath3 = FilePath2 + '\\'+ str(stockcode) + 'D.xls'
        DayData = Get_TrdData_FromExcel(FilePath3,'DataAvgLine')
        startDate = get_Trday_of_day(200,'5')
        FiveData = Get_TrData_FromTs(stockcode,'5')
        totalrows2 = len(DayData) #交易数据总量
        preDayClose = DayData.loc[totalrows2-1,'close']
        preDayAvg = DayData.loc[totalrows2-1,'Avg20']
        pre20DayClose = DayData.loc[totalrows2-20,'close']
        FiveMClose =  Last_Value_inCol(FiveData,'close')
        curAvg20 = (preDayAvg*20 - pre20DayClose + FiveMClose)/20
        if(FiveMClose > curAvg20):
            s = stockcodelist.iloc[irows]
            dfup = dfup.append(s)
            print('up')
        else:
            s = stockcodelist.iloc[irows]
            dfdown = dfdown.append(s)
            print('down')
        irows = irows + 1
    dfup = ReIndex(dfup)
    dfdown = ReIndex(dfdown)
    Write_DF_T0_Excel(FilePathBelow,dfdown,'codelist')
    Write_DF_T0_Excel(FilePathUp,dfup,'codelist')


#策略，用现货指数指导期货指数
def Buy_Sell_MoNi():
    stockcode='hs300'
    AnaCycle = 'D'
    FilePath = 'D:\Chan Data\LSHedge'
    AvgLine = 20
    MVAg_WZ(stockcode,AnaCycle,FilePath,AvgLine)
    XH_Data = SigAvgL_Buy_Sell(stockcode,AnaCycle,FilePath,AvgLine)
    AnaCycle = 'QD'
    QH_Data = MVAg_WZ(stockcode,AnaCycle,FilePath,AvgLine)
    irows = 0
    totalrows = len(XH_Data)
    QH_Data['操作'] = '无'
    while(irows < totalrows):
        QH_Data.loc[irows,'操作'] = XH_Data.loc[irows,'操作']
        irows = irows + 1
    sheetname = 'DataAvgLine'
    FilePath2 = FilePath + '\\'+'hs300QD20.xls'
    Write_DF_T0_Excel(FilePath2,QH_Data,sheetname)
    AvgL_curLong(stockcode,AnaCycle,FilePath,AvgLine)
    AvgL_curShort(stockcode,AnaCycle,FilePath,AvgLine)


#将带20日均线的数据下载到指定文件夹,n代表起始日期与当下时间的距离
def hs300_Avg_Down(n=0):
    #将沪深300的数据加上均线及均线位置，输入到指定的文件夹
    Stock_Code_list = get_hs300stock()
    Stock_Code_list = ReIndex(Stock_Code_list)
    FilePath = 'D:\Chan Data\AvgLData\HisData'
    AnaCycle = 'D'
    startDate = get_Trday_of_day(n+119,'D')
    endDate = get_Trday_of_day(n,'D')
    AvgLine = 20
    AboveCounter,BelowCounter,df = StockList_AvgData_Down(Stock_Code_list,FilePath,AnaCycle,startDate,endDate,AvgLine)
    df = ReIndex(df)
    print(AboveCounter,BelowCounter)
    FilePath2 = 'D:\Chan Data\AvgLData\StockBelow.xls'
    Write_DF_T0_Excel(FilePath2,df,'BelowList')


#单均线策略净值：
def sig_Avg_NV(stockcode='sz',AnaCycle='D',FilePath='FilePath',AvgLine=30):
    MVAg_WZ(stockcode,AnaCycle,FilePath,AvgLine)
    SigAvgL_Buy_Sell(stockcode,AnaCycle,FilePath,AvgLine)
    AvgL_curLong(stockcode,AnaCycle,FilePath,AvgLine)
    AvgL_curShort(stockcode,AnaCycle,FilePath,AvgLine)

#单均线策略评价
def sig_Avg_Comm(stockcode='sz',AnaCycle='D',FilePath='FilePath',AvgLine=30):
    MVAg_WZ(stockcode,AnaCycle,FilePath,AvgLine)
    SigAvgL_Buy_Sell(stockcode,AnaCycle,FilePath,AvgLine)
    AvgL_Long(stockcode,AnaCycle,FilePath,AvgLine)
    MACD_MAL_Long_Comm(stockcode,AnaCycle,FilePath,AvgLine)
    AvgL_Short(stockcode,AnaCycle,FilePath,AvgLine)
    MACD_MAL_Short_Comm(stockcode,AnaCycle,FilePath,AvgLine)

#单均线PE策略
def sig_Avg_PE_Comm(stockcode='sz',AnaCycle='D',FilePath='FilePath',AvgLine=30):
    MVAg_WZ(stockcode,AnaCycle,FilePath,AvgLine)
    SigAvgL_PE_Buy_Sell(stockcode,AnaCycle,FilePath,AvgLine)
    AvgL_Long(stockcode,AnaCycle,FilePath,AvgLine)
    MACD_MAL_Long_Comm(stockcode,AnaCycle,FilePath,AvgLine)
    AvgL_Short(stockcode,AnaCycle,FilePath,AvgLine)
    MACD_MAL_Short_Comm(stockcode,AnaCycle,FilePath,AvgLine)

#单均线均线方向策略
def sig_Avg_Dir_Comm(stockcode='sz',AnaCycle='D',FilePath='FilePath',AvgLine=30):
    MVAg_WZ_Dir(stockcode,AnaCycle,FilePath,AvgLine)
    SigAvgL_Dir_Buy_Sell(stockcode,AnaCycle,FilePath,AvgLine)
    AvgL_Long(stockcode,AnaCycle,FilePath,AvgLine)
    MACD_MAL_Long_Comm(stockcode,AnaCycle,FilePath,AvgLine)
    AvgL_Short(stockcode,AnaCycle,FilePath,AvgLine)
    MACD_MAL_Short_Comm(stockcode,AnaCycle,FilePath,AvgLine)

#单均线中枢策略：
def sig_Avg_ZS_Comm(stockcode='stockcode',AnaCycle='D',FilePath='FilePath',AvgLine=20):
    MVAg_WZ(stockcode,AnaCycle,FilePath,AvgLine)
    SigAvgL_ZS_Buy_Sell(stockcode,AnaCycle,FilePath,AvgLine)
    AvgL_Long(stockcode,AnaCycle,FilePath,AvgLine)
    MACD_MAL_Long_Comm(stockcode,AnaCycle,FilePath,AvgLine)
    AvgL_Short(stockcode,AnaCycle,FilePath,AvgLine)
    MACD_MAL_Short_Comm(stockcode,AnaCycle,FilePath,AvgLine)

##双均线中枢策略,一短一长
def dou_Avg_ZS_Comm(stockcode='sz',AnaCycle='D',FilePath='FilePath',AvgLS=5,AvgLL=10):
    DouMVAg_WZ(stockcode,AnaCycle ,FilePath,AvgLS,AvgLL)
    DouAvgL_ZS_Buy_Sell(stockcode,AnaCycle ,FilePath,AvgLS,AvgLL)
    DouAvgL_Long(stockcode,AnaCycle ,FilePath,AvgLS,AvgLL)
    DouMACD_MAL_Long_Comm(stockcode,AnaCycle,FilePath,AvgLS,AvgLL)
    DouAvgL_Short(stockcode,AnaCycle ,FilePath,AvgLS,AvgLL)
    DouMACD_MAL_Short_Comm(stockcode,AnaCycle,FilePath,AvgLS,AvgLL)


#双均线策略,一短一长
def dou_Avg_Comm(stockcode='sz',AnaCycle='D',FilePath='FilePath',AvgLS=5,AvgLL=10):
    DouMVAg_WZ(stockcode,AnaCycle ,FilePath,AvgLS,AvgLL)
    DouAvgL_Buy_Sell(stockcode,AnaCycle ,FilePath,AvgLS,AvgLL)
    DouAvgL_Long(stockcode,AnaCycle ,FilePath,AvgLS,AvgLL)
    DouMACD_MAL_Long_Comm(stockcode,AnaCycle,FilePath,AvgLS,AvgLL)
    DouAvgL_Short(stockcode,AnaCycle ,FilePath,AvgLS,AvgLL)
    DouMACD_MAL_Short_Comm(stockcode,AnaCycle,FilePath,AvgLS,AvgLL)


#数据转换,将从万得下载的交易数据，不含PE和PB数据
def Data_Transfer(SFilePath = 'D:\Chan Data\万得',SFileName = '沪深300+5分钟数据.xls',
                  TFilePath = 'D:\Chan Data\MACDData\EMV',TFileName = 'hs3005.xls'):
    SFilePath = SFilePath + '\\'+ SFileName
    TFilePath = TFilePath + '\\'+TFileName
    dateName='日期'
    openName = '开盘价(元)'
    highName ='最高价(元)'
    lowName = '最低价(元)'
    closeName= '收盘价(元)'
    sheetName = 'file'
    TrData_Trans(SFilePath,TFilePath,sheetName,dateName,openName,highName,lowName,closeName)

#数据转换程序2：将从万得下载的交易数据，转成Tushare能处理的形态。
#数据转换,将从万得下载的交易数据，不含PE和PB数据
def Data_Transfer2(SFilePath = 'D:\Chan Data\万得',SFileName = '沪深300+5分钟数据.xls',
                  TFilePath = 'D:\Chan Data\MACDData\EMV',TFileName = 'hs3005.xls'):
    SFilePath = SFilePath + '\\'+ SFileName
    TFilePath = TFilePath + '\\'+TFileName
    dateName='日期'
    openName = '开盘价(元)'
    highName ='最高价(元)'
    lowName = '最低价(元)'
    closeName= '收盘价(元)'
    peName = '市盈率'
    pbName = '市净率'
    sheetName = 'file'
    TrData_Trans2(SFilePath,TFilePath,sheetName,dateName,openName,highName,lowName,closeName,peName,pbName)


'''
 #MACD黄白线买入卖出程序
#将数据的DIF，DEA处理完毕，并存在Excel中,仅第一次使用,这个计算用的MV
    DouAvgL_Short(stockcode,AnaCycle ,FilePath,AvgLS,AvgLL)
    DouMACD_MAL_Short_Comm(stockcode,AnaCycle,FilePath,AvgLS,AvgLL)

    stockcode='道琼斯工业'
    AnaCycle ='D'
    FilePath = 'D:\Chan Data\MACDData\EMV'
    MACD_DIF_DEA_MV(stockcode,AnaCycle,FilePath)
    MACD_Buy_Sell_Plus(stockcode,AnaCycle,FilePath)
    MACD_Buy_Sell(stockcode,AnaCycle,FilePath)
    MACD_YWL_Long(stockcode,AnaCycle,FilePath)
    MACD_YWL_Long_Comm(stockcode,AnaCycle,FilePath)
    MACD_YWL_Short(stockcode,AnaCycle,FilePath)
    MACD_YWL_Short_Comm(stockcode,AnaCycle,FilePath)

    SFilePath = 'D:\Chan Data\万得'
    SFileName = '道琼斯工业.xls'
    SFilePath = SFilePath + '\\'+ SFileName
    TFilePath = 'D:\Chan Data\MACDData\EMV'
    TFileName = '道琼斯工业D.xls'
    TFilePath = TFilePath + '\\'+TFileName
    dateName='日期'
    openName = '开盘价(元)'
    highName ='最高价(元)'
    lowName = '最低价(元)'
    closeName= '收盘价(元)'
    sheetName = 'file'
    TrData_Trans(SFilePath,TFilePath,sheetName,dateName,openName,highName,lowName,closeName)
'''


#    MACD_DIF_DEA_MV(stockcode,AnaCycle,FilePath)
#    MACD_Buy_Sell(stockcode,AnaCycle,FilePath)
#    MACD_YWL_Long(stockcode,AnaCycle,FilePath)
#    MACD_YWL_Long_Comm(stockcode,AnaCycle,FilePath)
#    MACD_YWL_Short(stockcode,AnaCycle,FilePath)
#    MACD_YWL_Short_Comm(stockcode,AnaCycle,FilePath)


#这个计算移动平均用的EMA
#    stockcode='399106'
#    AnaCycle ='D'
#    FilePath = 'D:\Chan Data\MACDData\EMV'
#    MACD_DIF_DEA_EMV(stockcode,AnaCycle,FilePath)
#    MACD_Buy_Sell(stockcode,AnaCycle,FilePath)
#    MACD_YWL_Long(stockcode,AnaCycle,FilePath)
#    MACD_YWL_Long_Comm(stockcode,AnaCycle,FilePath)









