# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from DataProcess import *
from DataInter import *
from DataPlot import *
import datetime
from GenProcess import *
import pandas as pd
#数据展示和处理应用的子函数
#子函数1：根据输入的股票代码和分析周析，展示股票在相应周期的分笔图，同时输出最后一笔的起始时间和笔方向
def Lv1Process(StockCode = 'sh',AnaCycle = 'D'):
    S_Trd_Data = Get_TrData_FromTs (StockCode = StockCode,AnaCycle = AnaCycle)
    S_Trd_Data =  Data_MACD_BAR(S_Trd_Data)
    S_Trd_Data = Data_MFI(S_Trd_Data)
    Inclu_Data = Include(S_Trd_Data)
    IniFX_Data = AllFX(Inclu_Data)
    RealFX_Data = TopBottomDistin(IniFX_Data)
    Bi_Data,BiCounter = Bee(RealFX_Data)
    if(BiCounter < 3):
        Bi_Data = Bee_Update(Bi_Data,Inclu_Data)
        Pivot_Data = BiPivot(Bi_Data)
        print('No enough Bi')
    else:
        Bi_Data = Bee_Update(Bi_Data,Inclu_Data)
        Bi_Data = Bee_TLidu(Bi_Data,S_Trd_Data)
        Bi_Data = Bee_LLidu(Bi_Data,S_Trd_Data)
        Bi_Data = Bee_BarLidu(Bi_Data,S_Trd_Data)
        Bi_Data = Bee_MFILidu(Bi_Data,S_Trd_Data)
        Pivot_Data = BiPivot(Bi_Data)
    totalrows = len(S_Trd_Data)
    Date = S_Trd_Data.loc[totalrows-1,'date']
    FilePath = 'D:\Chan Data\Data'+'\\'+StockCode +'LV'+AnaCycle +'.xls'
    Write_To_Excel(FilePath,S_Trd_Data,Inclu_Data,IniFX_Data,RealFX_Data,Bi_Data,Pivot_Data)
    BiPlot(Bi_Data)
    totalrows = len(Bi_Data.index)
    LastBiStDate = Bi_Data.loc[totalrows-1,'startDate']
    LastBiTrend = Bi_Data.loc[totalrows-1,'Direc']
    return LastBiStDate , LastBiTrend
#子函数2：根据输入的代码和级别，起始日期以及笔方向，显示股票在当下周期的走势情况，并将数据存储至Excel,特别适用于与级别联立使用
def Lv2Process(StockCode = 'sh',AnaCycle = '30',startDate = 'startDate',endData = 'endDate',LastBiTrend = '无'):
    S_Trd_Data = Get_TrData_FromTs (StockCode = StockCode,AnaCycle = AnaCycle,startDate = startDate)
#    totalrows = len(S_Trd_Data.index)
#    S_Trd_Data.loc[totalrows-1,'date']= '2016-01-15 15:00:00'
    S_Trd_Data =  Data_MACD_BAR(S_Trd_Data)
    S_Trd_Data = Data_MFI(S_Trd_Data)
    Inclu_Data = Include(S_Trd_Data)
    IniFX_Data = AllFX(Inclu_Data)
    RealFX_Data = TopBottomDistin(IniFX_Data)
    Bi_Data,BiCounter = Bee(RealFX_Data)
    Bi_Data = Bee_Update(Bi_Data,Inclu_Data)
    if(BiCounter < 3):
        Bi_Data = Bee_TLidu(Bi_Data,S_Trd_Data)
        Bi_Data = Bee_LLidu(Bi_Data,S_Trd_Data)
        Bi_Data = Bee_BarLidu(Bi_Data,S_Trd_Data)
#        Bi_Data = Bee_MFILidu(Bi_Data,S_Trd_Data)
        Pivot_Data = BiPivot(Bi_Data,LastBiTrend)
        print('No enough Bi')
    else:
        Bi_Data = Bee_TLidu(Bi_Data,S_Trd_Data)
        Bi_Data = Bee_LLidu(Bi_Data,S_Trd_Data)
        Bi_Data = Bee_BarLidu(Bi_Data,S_Trd_Data)
        Bi_Data = Bee_MFILidu(Bi_Data,S_Trd_Data)
        Pivot_Data = BiPivot(Bi_Data,LastBiTrend)
    totalrows = len(S_Trd_Data)
    Date = S_Trd_Data.loc[totalrows-1,'date']
    FilePath = 'D:\Chan Data\Data'+'\\'+StockCode +'LV'+AnaCycle +'.xls'
    Write_To_Excel(FilePath,S_Trd_Data,Inclu_Data,IniFX_Data,RealFX_Data,Bi_Data,Pivot_Data)
    BiPlot(Bi_Data)
    totalrows = len(Bi_Data.index)
    LastBiStartDate = Bi_Data.loc[totalrows-1,'startDate']
    return LastBiStartDate

#股票选择用到的子函数
#选股函数1
# 找出给定股票列表中（参数stock_code_list）所有近N(由参数输入)个交易周期中以底分型结束的股票
def get_stock_end_bot(stock_code_list = 'stock_code_list',begindate ='begindate',enddate = 'enddate',AnaCycle='D'):
    stock_code_rst = []
    for stockcode in stock_code_list['stockcode']:
        stockcode = codeType(stockcode)
        print(stockcode)
        Trd_Data = Get_TrData_FromTs(StockCode=stockcode,AnaCycle=AnaCycle,startDate=begindate,endDate=enddate)
        totalrows = len(Trd_Data.index)
        if(totalrows >= 3): #用于处理停牌的股票
            Trd_Data = Include(Trd_Data)
            totalrows = len(Trd_Data.index)
            if(totalrows >= 3):
                irows = totalrows -2
                PriceHigh = Trd_Data.loc[irows,'high']
                PriceLow = Trd_Data.loc[irows,'low']
                prePriceHigh = Trd_Data.loc[irows-1 ,'high']
                prePriceLow = Trd_Data.loc[irows-1  ,'low']
                nxtPriceHigh = Trd_Data.loc[irows+1,'high']
                nxtPriceLow = Trd_Data.loc[irows+1 ,'low']
                if (PriceHigh < prePriceHigh) and (PriceLow < prePriceLow) and\
                    (PriceLow < nxtPriceLow) and (PriceLow < nxtPriceLow):
                    print(True)
                    stock_code_rst.append(stockcode)
        '''
        Trd_Data = Include(Trd_Data)
        totalrows = len(Trd_Data)
        if(totalrows >= 3):
            lastFX = WhatFX(Trd_Data,totalrows -2)
            if(lastFX == -1):
                stock_code_rst.append(stockcode)
        '''
    return stock_code_rst
#选股函数1.1，最近三天为下降K线
def get_stock_end_dkx(stock_code_list = 'stock_code_list',begindate ='begindate',enddate = 'enddate',AnaCycle='D'):
    stock_code_rst = []
    for stockcode in stock_code_list['stockcode']:
        stockcode = codeType(stockcode)
        print(stockcode)
        Trd_Data = Get_TrData_FromTs(StockCode=stockcode,AnaCycle=AnaCycle,startDate=begindate,endDate=enddate)
        totalrows = len(Trd_Data.index)
        if(totalrows >= 3): #用于处理停牌的股票
            Trd_Data = Include(Trd_Data)
            totalrows = len(Trd_Data.index)
            if(totalrows >= 3):
                irows = totalrows -2
                PriceHigh = Trd_Data.loc[irows,'high']
                PriceLow = Trd_Data.loc[irows,'low']
                prePriceHigh = Trd_Data.loc[irows-1 ,'high']
                prePriceLow = Trd_Data.loc[irows-1  ,'low']
                nxtPriceHigh = Trd_Data.loc[irows+1,'high']
                nxtPriceLow = Trd_Data.loc[irows+1 ,'low']
                if (PriceHigh < prePriceHigh) and (PriceLow < prePriceLow) and\
                    (PriceLow > nxtPriceLow) and (PriceLow > nxtPriceLow):
                    stock_code_rst.append(stockcode)
    return stock_code_rst
#选股函数2
# 选出在特定时间段的选定周期内出现三买的股票
#第2步处理，被调用
def ThirdBExist(StockCode = 'sh',AnaCycle = '5',startDate = 'startDate',endData = '',LastBiTrend = '下'):
    Trd_Data = Get_TrData_FromTs(StockCode=StockCode,AnaCycle=AnaCycle,startDate=startDate,endDate = endData)
    Inclu_Data = Include(Trd_Data)
    IniFX_Data = AllFX(Inclu_Data)
    RealFX_Data = TopBottomDistin(IniFX_Data)
    Bi_Data, BiCounter = Bee(RealFX_Data)
    thirdBuyExist = False
    if (BiCounter == 0):
        return thirdBuyExist
    else:
        thirdBuyExist = BiThirdBuy(Bi_Data,LastBiTrend)
        return thirdBuyExist
#第1步处理，调用
def get_stock_With_3Buy(stock_code_list = 'stock_code_list',AnaCycle = '5',begindate ='',enddate = '',Direc = '下'):
    stock_code_rst = []
    icounter = 0
    for stockcode in stock_code_list:
        stockcode = codeType(stockcode)
        print(stockcode)
        ThirdBuyExist = ThirdBExist(stockcode, AnaCycle,begindate,enddate,'下')
        print(ThirdBuyExist)
        if(ThirdBuyExist):
            stock_code_rst.append(stockcode)
    return stock_code_rst

#选股函数3
#开山盘背,取当下或上一与输入方向的笔与前前笔盘背
def IsPanBei(StockCode = 'sh',AnaCycle = '30',startDate = 'startDate',endData = 'endData',Dir = '下'):
    Trd_Data = Get_TrData_FromTs(StockCode=StockCode,AnaCycle=AnaCycle,startDate=startDate,endDate = endData)
    if(len(Trd_Data)>=60):
        Inclu_Data = Include(Trd_Data)
        IniFX_Data = AllFX(Inclu_Data)
        RealFX_Data = TopBottomDistin(IniFX_Data)
        Bi_Data, BiCounter = Bee(RealFX_Data)
        Bi_Data = Bee_Update(Bi_Data,Trd_Data)
        IsPanBei = False
        if (BiCounter < 3):
            return IsPanBei, BiCounter
        else:
            Bi_Data =  Bee_TLidu(Bi_Data,Trd_Data)
            totalrows = len(Bi_Data)
            Direc = Bi_Data.loc[totalrows-1,'Direc']
            if(Direc == Dir):
                HiLow = Bi_Data.loc[totalrows-1,'HiLow']
                Lidu = Bi_Data.loc[totalrows-1,'Lidu']
            else:
                Direc = Bi_Data.loc[totalrows-2,'Direc']
                HiLow = Bi_Data.loc[totalrows-2,'HiLow']
                Lidu = Bi_Data.loc[totalrows-2,'Lidu']
            if (Direc == '下') and (Direc == Dir):
                if(Lidu =='弱') and (HiLow == '低'):
                    IsPanBei = True
                elif(Lidu == '强'):
                    if(HiLow == '高') or (HiLow =='前包'):
                        IsPanBei = True
            elif (Direc == '上') and (Direc == Dir):
                if(Lidu =='弱'):
                    IsPanBei = True
                elif(Lidu == '强'):
                    if(HiLow == '低') or (HiLow =='前包'):
                        IsPanBei = True
    else:
        IsPanBei = False
        BiCounter = 0
    return IsPanBei, BiCounter

def get_stock_panbei(stock_code_list = 'stock_code_list',AnaCycle = '30',begindate='',enddate='',Dir = '下'):
    stock_code_rst = []
    icounter = 0
    for stockcode in stock_code_list:
        print(stockcode)
        stockcode = codeType(stockcode)
        PanBei,BiCounter = IsPanBei(stockcode, AnaCycle,begindate,enddate,Dir)
        print(PanBei,BiCounter)
        if(PanBei):
            stock_code_rst = stock_code_rst.append(stockcode)
    return stock_code_rst


#经典盘背，仅包含下低弱和上高弱
def IsPanBeiCla(StockCode = 'sh',AnaCycle = '30',startDate = 'startDate',endData = 'endData',Dir = '下'):
    Trd_Data = Get_TrData_FromTs(StockCode=StockCode,AnaCycle=AnaCycle,startDate=startDate,endDate = endData)
    #粗陋的容错处理，以后应该重的更好
    if(len(Trd_Data)>=60):
        Inclu_Data = Include(Trd_Data)
        IniFX_Data = AllFX(Inclu_Data)
        RealFX_Data = TopBottomDistin(IniFX_Data)
        Bi_Data, BiCounter = Bee(RealFX_Data)
        Bi_Data = Bee_Update(Bi_Data,Trd_Data)
        IsPanBei = False
        if (BiCounter < 3):
            return IsPanBei, BiCounter
        else:
            Bi_Data =  Bee_TLidu(Bi_Data,Trd_Data)
            totalrows = len(Bi_Data)
            Direc = Bi_Data.loc[totalrows-1,'Direc']
            if(Direc == Dir):
                HiLow = Bi_Data.loc[totalrows-1,'HiLow']
                Lidu = Bi_Data.loc[totalrows-1,'Lidu']
            else:
                Direc = Bi_Data.loc[totalrows-2,'Direc']
                HiLow = Bi_Data.loc[totalrows-2,'HiLow']
                Lidu = Bi_Data.loc[totalrows-2,'Lidu']
            if (Direc == '下') and (Direc == Dir):
                if(Lidu =='弱') and (HiLow == '低'):
                    IsPanBei = True
            elif (Direc == '上') and (Direc == Dir):
                if(Lidu =='弱') and (HiLow =='高'):
                    IsPanBei = True
    else:
        IsPanBei = False
        BiCounter = 0
    return IsPanBei, BiCounter

def get_stock_panbeiCla(stock_code_list = 'stock_code_list',AnaCycle = '30',begindate='',enddate='',Dir = '下'):
    stock_code_rst = []
    icounter = 0
    for stockcode in stock_code_list:

        stockcode = codeType(stockcode)
        PanBei,BiCounter = IsPanBeiCla(stockcode, AnaCycle,begindate,enddate,Dir)
#        print(PanBei,BiCounter)
        if(PanBei):
            stock_code_rst.append(stockcode)
    return stock_code_rst

#选股函数4
# 判断某支股票最近n日内是否出现tol个交易日以来的最低点，如果是返回True,否则返回False
def Lowest_in_Recent(StockCode ='sh',startDate='startDate',endDate='endDate',n=3):
    IsLowestIn = True
    Trd_Data = Get_TrData_FromTs(StockCode=StockCode,AnaCycle='D',startDate=startDate,endDate=endDate)
    irows = 1
    totalrows = len(Trd_Data.index)
    if(totalrows >= 1):
        LowestPrice = Trd_Data.loc[totalrows-1,'low']
        while(irows <= n) and (irows <= totalrows):
            LowPrice = Trd_Data.loc[totalrows - irows,'low']
            if(LowPrice < LowestPrice):
                LowestPrice = LowPrice
            irows = irows + 1
        while(irows <= totalrows):
            LowPrice = Trd_Data.loc[totalrows - irows,'low']
            if(LowPrice < LowestPrice):
                IsLowestIn = False
                break
            irows = irows + 1
    return IsLowestIn
#用全部数据的结果是处理时间过长，本意是处理n天内见total天新低的股票，
def Get_LowStock(stock_code_list='stock_code_list',startDate='startDate',endDate = 'endDate',n=3):
    stock_code_rst = []
    for stockcode in stock_code_list['stockcode']:
        print(stockcode)
        stockcode = codeType(stockcode)
        IsLowestIn = Lowest_in_Recent(stockcode,startDate,endDate,n)
        if(IsLowestIn):
#            print(IsLowestIn)
            stock_code_rst.append(stockcode)
    Write_to_txt('LowInRec.txt',stock_code_rst)
    stock_code_list = Read_from_txt(fileName = 'LowInRec.txt')
    FilePath = 'D:\Chan Data\Selected Stock\Str3\Date'+endDate+ '.xls'
    Write_STo_Excel(FilePath ,stock_code_list,'StockList')
    return stock_code_rst

#独立选股程序1,上涨下跌幅度
def UPDownList(n=0,total =20,Direc ='下'):
    FilePath = 'D:\Chan Data\Selected Stock\IndStock\StockUpDown.xls'
    list = get_all_stock()
    beginDate = get_Trday_of_day(n+total)
    endDate = get_Trday_of_day(n)
    RiseDownList = UpDownInCycle(list,beginDate,endDate,Direc)
    Write_DF_T0_Excel(FilePath,RiseDownList)
    return RiseDownList

def UpDownInCycle(stock_code_list='stock_code_list',begindate = 'begindate',enddate = 'enddate',Direc = '下'):
    stokupdown =DataFrame
    RiseDownList = DataFrame(columns=['stockcode','updown'])
    for stockcode in stock_code_list['stockcode']:
        stockcode = codeType(stockcode)
        Trd_Data = Get_TrData_FromTs(StockCode=stockcode,AnaCycle='D',startDate=begindate,endDate=enddate)
        totalrows = len(Trd_Data)
        if(totalrows>=2):
            beginPrice =Trd_Data.loc[0,'close']
            endPrice = Trd_Data.loc[totalrows-1,'close']
            updownPer = (endPrice-beginPrice)/beginPrice
            s = Series([stockcode,updownPer],index=['stockcode','updown'])
        else:
            updownPer = 0
            s = Series([stockcode,updownPer],index=['stockcode','updown'])
        RiseDownList = RiseDownList.append(s,ignore_index=True)
        if(Direc =='下'):
            RiseDownList.sort_values(by='updown',ascending=True)
        elif(Direc =='上'):
            RiseDownList.sort_values(by='updown',ascending=False)
    return RiseDownList


#独立选股程序2，各个股票的波动率，其中波动详率用方差
def VolaList(n=0,total =700,AnaCycle ='D'):
    FilePath = 'D:\Chan Data\Selected Stock\VolStock\StockVol.xls'
    list = get_all_stock()
    beginDate = get_Trday_of_day(n+total)
    endDate = get_Trday_of_day(n)
    VolaList = VolaInCycle(list,beginDate,endDate,AnaCycle)
    Write_DF_T0_Excel(FilePath,VolaList)
    return VolaList

def VolaInCycle(stock_code_list='stock_code_list',begindate = 'begindate',enddate = 'enddate',AnaCycle ='D'):
    VarList = DataFrame(columns=['stockcode','stockVar'])
    for stockcode in stock_code_list['stockcode']:
        stockcode = codeType(stockcode)
        print(stockcode)
        Trd_Data = Get_TrData_FromTs(StockCode=stockcode,AnaCycle='D',startDate=begindate,endDate=enddate)
        totalrows = len(Trd_Data)
        stockVar = Stock_Vol(stockcode,AnaCycle,begindate,enddate)
        s = Series([stockcode,stockVar],index=['stockcode','stockVar'])
        VarList = VarList.append(s,ignore_index=True)
    VarList.sort_values(by='stockVar',ascending=False)
    return VarList

#对于任意证券，返回其最近的中枢
def Lastest_ZS(stockcode = 'sh',AnaCycle = 'D',startDate = 'startDate',endDate ='endDate',n=0):
    date = get_Trday_of_day(n)
    FilePath = 'D:\Chan Data\MrkData'+'\\'+date+'\\'+stockcode+ '.xls'
    Bi_Data = pd.read_excel(io=FilePath,sheetname = 'DBi')
    BiCounter = len(Bi_Data)
    if(BiCounter < 3):
        Pivot_Data = BiPivot(Bi_Data)
        print('No enough Bi')
    else:
        Pivot_Data = BiPivot(Bi_Data)
    ZSExist,zs_data = ZhongShu(Pivot_Data)
    return ZSExist,zs_data,Pivot_Data



#中枢位置关系：对于任意证券，得出最新收盘价与最近中枢的位置关系,两个维度一个是上中下，一个是位置(具体区间)
def ZS_WZR(stockcode = 'sh',AnaCycle = 'D',startDate = 'startDate',endDate ='endDate'):
    ZSExist,zs_data,Pivot_Data = Lastest_ZS(stockcode ,AnaCycle,startDate ,endDate)
    if (ZSExist == False):
        ZSR1 = '无'
        ZSR2 = '无'
        zs_data['GG'] = '无'
        zs_data['DD'] = '无'
        zs_data['ZG'] = '无'
        zs_data['ZD'] = '无'
        return zs_data,ZSR1,ZSR2,Pivot_Data
    else:
        close = Latest_Close(stockcode,AnaCycle)
        GG = zs_data['GG']
        DD = zs_data['DD']
        ZG = zs_data['ZG']
        ZD = zs_data['ZD']
        if(close >GG):
            ZSR1 = '上'
            ZSR2 = 'GG之上'
        elif(close > ZG) and (close< GG):
            ZSR1 = '上'
            ZSR2 = 'ZG与GG之间'
        elif (close > ZD) and (close< ZG):
            ZSR1 = '中'
            ZSR2 = '中枢中'
        elif (close > DD) and (close< ZD):
            ZSR1 = '下'
            ZSR2 = 'DD与ZD之间'
        else:
            ZSR1 = '下'
            ZSR2 = 'DD之下'
    return zs_data,ZSR1,ZSR2,Pivot_Data

#大盘走势统计程序,统计与中枢位置关系
def ZSWZ_Stat(stockcode ='sh',n=0,AnaCycle='D'):
    startDate = get_Trday_of_day(n+120)
    endDate = get_Trday_of_day(n)
    zs_data,ZSR1,ZSR2,Pivot_Data = ZS_WZR(stockcode,AnaCycle,startDate,endDate)
    return zs_data,ZSR1,ZSR2,Pivot_Data
#    zs_gx_data = Series(zs_data.values,ZSR1,ZSR2,columns =['','','',])
#三买正在形成中：
#def ThridBinPro():











