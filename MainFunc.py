 # -*- coding: utf-8 -*-
import datetime
from StrApplication import *
from AppTest import *
from PerfComment import *
from GenProcess import *
from DataProcess import *
from MAMACDApplication import *

if __name__=="__main__":

    #展示各周期的笔，此处为每个日线笔对应的30分钟和5分钟内部结构
    FilPath = 'D:\Chan Data\BiDemo'
    stockcode = 'sz'
    FilePathDay = FilPath +'\\'+stockcode + 'D.xls'
    dayFrame = Get_TrdData_FromExcel(FilePathDay,'DBi')

    FilePath30 = FilPath +'\\'+stockcode + '30.xls'
    FilePath5 = FilPath +'\\'+stockcode + '5.xls'
    thirFrame =  Get_TrdData_FromExcel(FilePath30,'30Bi')
    fiveFrame = Get_TrdData_FromExcel(FilePath5,'5Bi')
    BiDemo(dayFrame,thirFrame,fiveFrame)

#第二层统计
#    Stockcode = '600570'
#    Anacycle = 'D'
#    startDate = get_Trday_of_day(700,Anacycle)
#    endDate = get_Trday_of_day(0,Anacycle)
#    Lv2Process(Stockcode,Anacycle,startDate,endDate)

#    Lv1Process(Stockcode,'5')
#选股第一步：数据准备工作，将有成交的数据下载到D:\Chan Data\Source
#得到日线级别、30分钟级别120个交易单元内交易>80%的股票,然代码名单存入指定的文件路径中，函数存储在Elimi_No_Trade中
#由于实际过程中，为统计一二三买，至少应该有大于5笔数据
#    FilePath = 'D:\Chan Data\Source\沪深300数据'
#    n = 0
#    Elimi_No_Trade_Down(FilePath,120,0.8,'D',n)
#    Elimi_No_Trade_Down(FilePath,120,0.8,'30',n*8)
#    SCycle='D'
#    UpdCycle ='30'
#    Data_Update_Day(FilePath,SCycle,UpdCycle)


#选股第二步：选择三买和二买进行中的股票
#    FilePath = 'D:\Chan Data\Source\沪深300数据'
#    proDay = get_Trday_of_day(n,'D')
#    proDay = '2016-03-25'
#    proDay = get_Trday_of_day(1,'30')
#    proDay = proDay[0:10]
#    Sel_SecB_in_Pro(FilePath,0,'D',proDay)
#    Sel_TMB_in_Pro(FilePath,0,'30',proDay)
#    Sel_TMB_in_Pro(FilePath,0,'D',proDay)
#    Sel_SecB_in_Pro(FilePath,0,'30',proDay)

#用于找了突破大盘20日线的股票
#将300指数对应的股票数据下载过来,并将收盘仍处于20日下的股票存到表中
#    hs300_Avg_Down(0)
#对于数据表中的数据，选出当前收盘价高于和低于20日均价的股票
#    FilePath = 'D:\Chan Data\AvgLData'
#    Sel_Stock_Over_Avg(FilePath)


#将沪深300中有交易的数据下载到指定路径,包括源数据和笔数据
#    AnaCycle = '30'
#    stock_code_list = get_hs300stockOp(AnaCycle)
#    startDate = get_Trday_of_day(120,AnaCycle)
#    endDate = get_Trday_of_day(1,AnaCycle)
#    FilePath = 'D:\Chan Data\MrkData'
#    Stock_List_Data_Down(stock_code_list,FilePath,AnaCycle,startDate,endDate)

#将指定（Excel表中）的源数据，加工成笔数据，并存储在同样路径页中，页名为'AnaCycle+Bi'
#    FilePath ='D:\Chan Data\BiDemo'
#    stockcode = '汇川技术'
#    AnaCycle = ''
#    AddBiSheet(FilePath,stockcode,AnaCycle)



#计算所有股票在700个交易日内的波动率,以找出波动率最大或最小的股票：在某时间敬意内，涨跌幅最大最小，以及各指标都可统计
#    VolaList(0,700,'D')
#独立数据处理 将所有股票相应周期内的最大涨跌幅进行处理
#    UPDownList(0,25,'下')



#将沪深300中有交易的数据下载到指定路径,包括源数据和笔数据
#    AnaCycle = '30'
#    stock_code_list = get_hs300stockOp(AnaCycle)
#    startDate = get_Trday_of_day(120,AnaCycle)
#    endDate = get_Trday_of_day(1,AnaCycle)
#    FilePath = 'D:\Chan Data\MrkData'
#    Stock_List_Data_Down(stock_code_list,FilePath,AnaCycle,startDate,endDate)

#用个股统计大盘，统计各股票的中枢状态
#    FilePath = 'D:\Chan Data\Source\沪深300成份股.xlsx'
#    Elimi_No_Trade(FilePath,100,0.9,'D')
#    ZSWZ_Stat_300()






#对给出股票代码做全周期处理以及根据给出的时间区间处理走势
#    StockCode = '600518'
#    AllCyclePro(StockCode)

#    ZSGX_Stat(0,'30')

#策略三：30分钟三买
#     Sel_TM_3B(1)

#策略4
#    stock_code_list = Sel_XD_PB(n=0,tol = 120, rec = 3)

#找到日线3(可选)个交易日为连续下降K线（包含处理后）且30分钟属于盘背段的股票，如果总数小于40支，进一步限定日线盘背的股票
#     stock_code_list = Sel_Stock_PB3BDFX()
#     FilePath = 'D:\Chan Data\Selected Stock\Str1\Date2016-01-21.xls'
#     Sel_Stock_All_Cycle(FilePath = FilePath)

#评估策略选出股票在未来一天的表现，未来可以根据更长期的表现
#     stock_code_list = Get_LowStock()
#     print(stock_code_list)
#    enddate = get_Trday_of_day(0)
#    print(enddate)
#     startdate = get_Trday_of_day(4)
#     print(startdate)
#     FilePath = 'D:\Chan Data\Selected Stock\Date'+startdate+'.xls'
#     Sel_Stock_Perf(FilePath,enddate,startdate)

#     stock_code_list = Sel_Stock_PB3BDFX(n=0)
#    Sel_TM_3B(0)
#     Sel_Stock_DB3B(0)
#     SelStockPerf(n=2)

#选择股票在给定的买入卖出时间期间的表现
#     SellDate = get_Trday_of_day(1)
#     BuyDate = get_Trday_of_day(2)
#     Stock_Performance(SellDate,BuyDate)




#评价程序1：MFITrend的评价程序1
#    StockCode = '600535'
#    AnaCycle = 'D'
#    MFITrendStat(StockCode,AnaCycle)


#指定产品交易效率和效果的评价。
#    FileFolder = 'D:\Chan Data\OpeData'
#    ProductName = '知钱神农1号'
#    ProductName = '知钱神州1号'
#    SheetName = '交易记录'
#    OpeComment(FileFolder,ProductName,SheetName)

'''
'''
#输入日期，显示期间指定股标的涨跌幅
#    stockcode = 'cyb'
#    startdate = '2015-02-06'
#    enddate = '2015-06-08'
#    updownPer = UpDownPerc(stockcode,startdate,enddate)
#    print(updownPer)



































