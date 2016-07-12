 # -*- coding: utf-8 -*-
import datetime
from StrApplication import *
from AppTest import *
from PerfComment import *
from GenProcess import *
from DataProcess import *
from MAMACDApplication import *
from DataInter import *
from MAMACDPerf import *
if __name__=="__main__":
#用于找了突破大盘20日线的股票
#将300指数对应的股票数据下载过来,并将收盘仍处于20日下的股票存到表中
    hs300_Avg_Down(0)
#对于数据表中的数据，选出当前收盘价高于和低于收盘价格的股票
#    FilePath = 'D:\Chan Data\AvgLData'
#    Sel_Stock_Over_Avg(FilePath)


#单均线、加中枢策略净值
    stockcode='hs300'
    AnaCycle = 'QD'
    FilePath = 'D:\Chan Data\LSHedge'
#    Pivot_Data = AddPivotData(stockcode,AnaCycle,FilePath)
#    AvgLine = 20
    FilePath1 = FilePath + '\\'+stockcode + AnaCycle + '.xls'
#    PivotData = Get_TrdData_FromExcel(FilePath1,'QDBi')
#    PivotData = PivotData[:30]
#    BiPlot(PivotData)
#    AddZSWZ(stockcode,AnaCycle,FilePath)
#    sig_Avg_ZS_Comm(stockcode,AnaCycle,FilePath,AvgLine)
#    sig_Avg_Comm(stockcode,AnaCycle,FilePath,AvgLine)

#双均线加中枢策略净值
#    AvgLShort = 5
#    AvgLLong = 10
#    dou_Avg_ZS_Comm(stockcode,AnaCycle,FilePath,AvgLShort,AvgLLong)


#用指数的买卖操作指导期指
#    Buy_Sell_MoNi()
#单均线策略净值
#    stockcode='hs300'
#    AnaCycle = 'QD'
#    FilePath = 'D:\Chan Data\LSHedge'
#    AvgLine = 20
#    sig_Avg_NV(stockcode,AnaCycle,FilePath,AvgLine)



#对比2：55和收盘计算均线及信号的差别
#    DayFive_Compare()


#    FilePath1 = 'D:\Chan Data\MNicompare\hs300D.xls'
#    FilePath2 = 'D:\Chan Data\MNicompare\hs3005.xls'
#    Trd_Day = Get_TrdData_FromExcel(FilePath1,'OriData')
#    Trd_FiveM = Get_TrdData_FromExcel(FilePath2,'OriData')
#    DataSimu(Trd_Day ,Trd_FiveM )

#单均线+均线方向策略，当均线向下时，上穿不买，当均线向上时，下穿不卖
#    stockcode='hs300'
#    AnaCycle = 'D'
#    FilePath = 'D:\Chan Data\MADir'
#    AvgLine = 20
#    sig_Avg_Dir_Comm(stockcode,AnaCycle,FilePath,AvgLine)


'''
    #数据转换程序1
    SFilePath = 'D:\Chan Data\万得'
    SFileName = 'hs300QD.xls'
    TFilePath = 'D:\Chan Data\LSHedge'
#   TFileName = '东方财富.xls'
    TFileName = SFileName
    Data_Transfer(SFilePath,SFileName,TFilePath,TFileName)

 #单均线策略评价
    stockcode='hs300'
    AnaCycle = 'Q30'
    FilePath = 'D:\Chan Data\LSHedge'
    AvgLine = 30
    sig_Avg_Comm(stockcode,AnaCycle,FilePath,AvgLine)

    #数据转换程序1
    SFilePath = 'D:\Chan Data\万得'
    SFileName = 'hs300D.xls'
    TFilePath = 'D:\Chan Data\LSHedge'
#   TFileName = '东方财富.xls'
    TFileName = SFileName
    Data_Transfer(SFilePath,SFileName,TFilePath,TFileName)



 #单均线策略评价
    stockcode='hs300'
    AnaCycle = '30'
    FilePath = 'D:\Chan Data\MovingAvg\SigMA'
    AvgLine = 30
    sig_Avg_Comm(stockcode,AnaCycle,FilePath,AvgLine)

#单均线+均线方向策略，当均线向下时，上穿不买，当均线向上时，下穿不卖
#    stockcode='hs300'
#    AnaCycle = 'D'
#    FilePath = 'D:\Chan Data\MADir'
#    AvgLine = 20
#    sig_Avg_Dir_Comm(stockcode,AnaCycle,FilePath,AvgLine)

    #数据转换程序1
    SFilePath = 'D:\Chan Data\万得'
    SFileName = 'hs3005.xls'
    TFilePath = 'D:\Chan Data\MovingAvg\SigMA'
#   TFileName = '东方财富.xls'
    TFileName = SFileName
    Data_Transfer(SFilePath,SFileName,TFilePath,TFileName)

    #数据转换程序1
    SFilePath = 'D:\Chan Data\万得'
    SFileName = 'hs3005.xls'
    TFilePath = 'D:\Chan Data\MovingAvg\SigMA'
#   TFileName = '东方财富.xls'
    TFileName = SFileName
    Data_Transfer(SFilePath,SFileName,TFilePath,TFileName)


    #双均线策略评价
    stockcode='hs300'
    AnaCycle = '30'
    FilePath = 'D:\Chan Data\MovingAvg\DouMA'
    AvgLS = 10
    AvgLL = 30
    dou_Avg_Comm(stockcode,AnaCycle,FilePath,AvgLS,AvgLL)

    #单均线策略评价
    stockcode='海通证券'
    AnaCycle = ''
    FilePath = 'D:\Chan Data\MovingAvg\SigMA'
    AvgLine = 20
    sig_Avg_Comm(stockcode,AnaCycle,FilePath,AvgLine)

    #数据转换程序1
    SFilePath = 'D:\Chan Data\万得'
    SFileName = '海通证券.xls'
    TFilePath = 'D:\Chan Data\MovingAvg\SigMA'
#   TFileName = '东方财富.xls'
    TFileName = SFileName
    Data_Transfer(SFilePath,SFileName,TFilePath,TFileName)



    #数据转换程序1
    SFilePath = 'D:\Chan Data\万得'
    SFileName = '贵州茅台.xls'
    TFilePath = 'D:\Chan Data\MovingAvg\SigMA'
#   TFileName = '东方财富.xls'
    TFileName = SFileName
    Data_Transfer(SFilePath,SFileName,TFilePath,TFileName)

    #单均线策略结合PE评价
    stockcode='hs300'
    AnaCycle = 'D'
    FilePath = 'D:\Chan Data\MAPEPB'
    AvgLine = 30
    sig_Avg_PE_Comm(stockcode,AnaCycle,FilePath,AvgLine)


    stockcode='ic1603'
    AnaCycle = ''
    FilePath = 'D:\Chan Data\MovingAvg\SigMA'
    AvgLine = 20
    sig_Avg_Comm(stockcode,AnaCycle,FilePath,AvgLine)


#单均线策略评价
    stockcode='hs300'
    AnaCycle = 'D'
    FilePath = 'D:\Chan Data\MovingAvg\SigMA'
    AvgLine = 30
    sig_Avg_Comm(stockcode,AnaCycle,FilePath,AvgLine)

#单均线策略结合PE评价
    stockcode='hs300'
    AnaCycle = 'D'
    FilePath = 'D:\Chan Data\MAPEPB'
    AvgLine = 20
    sig_Avg_PE_Comm(stockcode,AnaCycle,FilePath,AvgLine)

    #双均线策略评价
    stockcode='ih1603'
    AnaCycle = ''
    FilePath = 'D:\Chan Data\MovingAvg\DouMA'
    AvgLS = 3
    AvgLL = 30
    dou_Avg_Comm(stockcode,AnaCycle,FilePath,AvgLS,AvgLL)

    #数据转换程序2，交易数据带PE，PB
    SFilePath = 'D:\Chan Data\万得'
    SFileName = '指数行情序列上证指数.xls'
    TFilePath = 'D:\Chan Data\MAPEPB'
    TFileName = 'shD.xls'
    Data_Transfer2(SFilePath,SFileName,TFilePath,TFileName)



#统计PE值的分布,并将之并到一张表中：
    FilePath = 'D:\Chan Data\MAPEPB'
    FileName = 'hs300D.xls'
    s_hs300 = PE_Statistic(FilePath,FileName)
    FileName = 'shD.xls'
    s_sh = PE_Statistic(FilePath,FileName)
    FileName = 'szD.xls'
    s_sz = PE_Statistic(FilePath,FileName)
    df_PEStat = DataFrame([],columns=s_hs300.index)
    df_PEStat = df_PEStat.append(s_hs300.T,ignore_index=True)
    df_PEStat = df_PEStat.append(s_sh.T,ignore_index=True)
    df_PEStat = df_PEStat.append(s_sz.T,ignore_index=True)

    df_PEStat = DataFrame(df_PEStat.values,index = ['沪深300','深成指','上证指'],columns=df_PEStat.columns)
    FilePath = 'D:\Chan Data\MAPEPB'+'\\'+'PEStat.xls'
    Write_DF_T0_Excel(FilePath,df_PEStat,'PE')


    #数据合并
    FilePath = 'D:\Chan Data\LSHedge'
    FileName = 'hs3003030AvgLShort.xls'
    FilePath = FilePath + '\\'+FileName
    Trd_Data = Get_TrdData_FromExcel(FilePath,'DataAvgLine')
    DateMerge(Trd_Data)
    '''