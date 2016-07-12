# -*- coding: utf-8 -*-
#一些数据类型的通用处理
from time import strftime, localtime
from datetime import timedelta, date,datetime
from pandas import DataFrame
import tushare as ts
import math
import types
from DataInter import *
from DataProcess import *
import os

#时间数据类型处理
#找到最后有交易记录的日期前n个交易日的日期，目前用的是系统表，整理一张交易日表也是好主意，未来处理，对效率有提升
def get_Trday_of_day(n = 0,AnaCycle ='D'):
    SH_Trd_Data = Get_TrData_FromTs(StockCode='sh',AnaCycle=AnaCycle)
    totalrows = len(SH_Trd_Data.index)
    tardate = SH_Trd_Data.loc[totalrows -n -1,'date']
    return tardate

#将任何类型的股票代码转换成本程序通用的代码，只是针对遇到的情况，未来要根据数据源升级
def codeType(stockcode = 'sh'):
    if type(stockcode) is str:
        if len(stockcode) == 8:
            stockcode = stockcode[1:7]
        elif len(stockcode) == 4:
            stockcode = stockcode[1:3]
        elif len(stockcode) == 9:
            stockcode = stockcode[2:8]
    else:
        stockcode = str(stockcode)
        stockcode = stockcode.zfill(6)
    return stockcode

#根据给出的代码返回股票的最近收盘价,如果20个交易日内有交易，返回最近成交价，否则返回无
def Latest_Close(StockCode = 'StockCode',Anacycle = 'D'):
    startdate = get_Trday_of_day(19)
    Trd_Data = Get_TrData_FromTs(StockCode,Anacycle,startdate)
    totalrows = len(Trd_Data)
    if(totalrows == 0):
        lastClose ='无'
    else:
        lastClose = Trd_Data.loc[totalrows-1,'close']
    return lastClose

#将浮点型数据转化成日期类型,格式为&Y&m%d
def flo_to_Date(Date ='Date'):
    Date = int(Date)
    Date = str(Date)
    dt = datetime.strptime(Date,'%Y%m%d')
    return dt

#对于输入的起止日期和股票代码，输出期间的涨跌比例
def UpDownPerc(stockcode='stockcode',begindate = 'begindate',enddate = 'enddate'):
    stockcode = codeType(stockcode)
    Trd_Data = Get_TrData_FromTs(StockCode=stockcode,AnaCycle='D',startDate=begindate,endDate=enddate)
    totalrows = len(Trd_Data)
    if(totalrows>=2):
        beginPrice =Trd_Data.loc[0,'close']
        endPrice = Trd_Data.loc[totalrows-1,'close']
        updownPer = (endPrice-beginPrice)/beginPrice
    else:
        updownPer = 0
    return updownPer

#重置DataFrame的序号为以0开始，差值为1的等差数列
def ReIndex(df = 'df'):
    df = DataFrame(df.values,columns = df.columns)
    return df

# 返回给出的DataFrmae中指定列的最后一个值,如果无值返回'无'
def  Last_Value_inCol (df = 'df',colname = 'colname'):
#    print(df)
    totalrows = len(df)
    irows = totalrows-1
    while(irows >= 0):
        curValue = df.loc[irows,colname]
        if(curValue=='无'):
            irows = irows -1
        else:
            break
    return curValue



#有交易的数据占总数据的比例
def trd_day_per(stockcode='stockcode',AnaCycle = 'D',startDate ='startDate',endDate='endDate',toldays = 'toldays'):
    trd_Data = Get_TrData_FromTs (stockcode,AnaCycle,startDate,endDate)
    totalrows = len(trd_Data)
    trd_per = totalrows/(toldays+1)
    return trd_per

#根据输入本级别的级别值，输出次级别值
def SubCycle(curCycle ='D'):
    if(curCycle == 'W'):
        subCycle = 'D'
    elif(curCycle == 'D'):
        subCycle = '30'
    elif(curCycle == '60'):
        subCycle = '15'
    elif(curCycle == '30'):
        subCycle = '5'
    elif(curCycle == '5'):
        subCycle = '5'
    return subCycle

#根据输入的盈亏值和数据表，计算盈亏次数
def WinLoss_Stat(UpDownPer=0,PerfStat='PerfStat'):
    if(UpDownPer > 0):
        PerfStat.loc['盈利','总次数'] = PerfStat.loc['盈利','总次数'] + 1
        if(UpDownPer > 0) and (UpDownPer<=0.05):
            PerfStat.loc['盈利','0-5'] = PerfStat.loc['盈利','0-5'] + 1
        elif(UpDownPer>0.05)and (UpDownPer<=0.1):
            PerfStat.loc['盈利','5-10'] = PerfStat.loc['盈利','5-10'] + 1
        elif(UpDownPer>0.1)and (UpDownPer<=0.15):
            PerfStat.loc['盈利','10-15'] = PerfStat.loc['盈利','10-15'] + 1
        elif(UpDownPer>0.15)and (UpDownPer<=0.2):
            PerfStat.loc['盈利','15-20'] = PerfStat.loc['盈利','15-20'] + 1
        elif(UpDownPer>0.2)and (UpDownPer<=0.3):
            PerfStat.loc['盈利','20-30'] = PerfStat.loc['盈利','20-30'] + 1
        elif(UpDownPer>0.3)and (UpDownPer<=0.5):
            PerfStat.loc['盈利','30-50'] = PerfStat.loc['盈利','30-50'] + 1
        elif(UpDownPer>0.5)and (UpDownPer<=1):
            PerfStat.loc['盈利','50-100'] = PerfStat.loc['盈利','50-100'] + 1
        elif(UpDownPer > 1):
            PerfStat.loc['盈利','>100'] = PerfStat.loc['盈利','>100'] + 1
    elif(UpDownPer < 0):
        PerfStat.loc['亏损','总次数'] = PerfStat.loc['亏损','总次数'] + 1
        if(UpDownPer < 0) and (UpDownPer>=-0.05):
            PerfStat.loc['亏损','0-5'] = PerfStat.loc['亏损','0-5'] + 1
        elif(UpDownPer<-0.05)and (UpDownPer>=-0.1):
            PerfStat.loc['亏损','5-10'] = PerfStat.loc['亏损','5-10'] + 1
        elif(UpDownPer<-0.1)and (UpDownPer>=-0.15):
            PerfStat.loc['亏损','10-15'] = PerfStat.loc['亏损','10-15'] + 1
        elif(UpDownPer<-0.15)and (UpDownPer>=-0.2):
            PerfStat.loc['亏损','15-20'] = PerfStat.loc['亏损','15-20'] + 1
        elif(UpDownPer<-0.2)and (UpDownPer>=-0.3):
            PerfStat.loc['亏损','20-30'] = PerfStat.loc['亏损','20-30'] + 1
        elif(UpDownPer<-0.3)and (UpDownPer>=-0.5):
            PerfStat.loc['亏损','30-50'] = PerfStat.loc['亏损','30-50'] + 1
        elif(UpDownPer<-0.5)and (UpDownPer>=-1):
            PerfStat.loc['亏损','50-100'] = PerfStat.loc['亏损','50-100'] + 1
        elif(UpDownPer < -1):
            PerfStat.loc['亏损','>100'] = PerfStat.loc['亏损','>100'] + 1
    return PerfStat

#根据输入的笔数据DataFrame,输出行情数据的起止日期
def Trd_TimeSpan(df ='df'):
    totalrows = len(df)
    startdate = df.loc[0,'startDate']
    enddate = df.loc[totalrows-1,'endDate']
    return startdate,enddate

#根据输入的DataFrame以及起止日期，返回笔数据
def Bi_in_time(df='df',startdate='startdate',enddate='enddate'):
    irows = 0
    totalrows = len(df)
    bi_Df = DataFrame([],columns=['startDate','endDate','startPrice','endPrice','Direc','TrDays','XL','HiLow','Lidu'])
    while(irows < totalrows):
        sdate = df.loc[irows,'startDate']
        edate = df.loc[irows,'endDate']
        if(sdate >= startdate) and (edate <= enddate):
            s =df.iloc[irows]
            bi_Df = bi_Df.append(s,ignore_index=True)
            irows = irows + 1
        elif (sdate < startdate):
            irows = irows + 1
        elif(sdate > enddate):
            break
        else:
            irows = irows + 1
    return bi_Df

#PE分类，看各区间内的PE值数量
def PE_Statistic(FilePath='FilePath',FileName='FileName'):
    FilePath = FilePath +'\\'+ FileName
    Trd_Data =Get_TrdData_FromExcel(FilePath,'OriData')
    Trd_Data = ReIndex(Trd_Data)
    s = Trd_Data['PE']
    totalrows = len(s)
    irows = 0
    PE_Distribute = Series([0,0,0,0,0,0,0,0,0,0,0,0,0,0],['0-5','5-10','10-15','15-20',
                '20-30','30-40','40-50','50-60','60-70','70-80','80-90','90-100','100-150','>150'])
    Max = s[irows]
    Min = s[irows]
    while(irows < totalrows):
        curPE = s[irows]
        if (Max < curPE):
            Max = curPE
        if(Min > curPE):
            Min = curPE
        if(0<curPE<=5):
            PE_Distribute['0-5'] = PE_Distribute['0-5'] + 1
        elif(5<curPE<=10):
            PE_Distribute['5-10'] = PE_Distribute['5-10'] + 1
        elif(10<curPE<=15):
            PE_Distribute['10-15'] = PE_Distribute['10-15'] + 1
        elif(15<curPE<=20):
            PE_Distribute['15-20'] = PE_Distribute['15-20'] + 1
        elif(20<curPE<=30):
            PE_Distribute['20-30'] = PE_Distribute['20-30'] + 1
        elif(30<curPE<=40):
            PE_Distribute['30-40'] = PE_Distribute['30-40'] + 1
        elif(40<curPE<=50):
            PE_Distribute['40-50'] = PE_Distribute['40-50'] + 1
        elif(50<curPE<=60):
            PE_Distribute['50-60'] = PE_Distribute['50-60'] + 1
        elif(60<curPE<=70):
            PE_Distribute['60-70'] = PE_Distribute['60-70'] + 1
        elif(70<curPE<=80):
            PE_Distribute['70-80'] = PE_Distribute['70-80'] + 1
        elif(80<curPE<=90):
            PE_Distribute['80-90'] = PE_Distribute['80-90'] + 1
        elif(90<curPE<=100):
            PE_Distribute['90-100'] = PE_Distribute['90-100'] + 1
        elif(100<curPE<=150):
            PE_Distribute['100-150'] = PE_Distribute['100-150'] + 1
        elif(curPE>150):
            PE_Distribute['>150'] = PE_Distribute['>150'] + 1
        irows = irows + 1
    return PE_Distribute

#新建文件夹的函数
def mkdir(path):
    # 引入模块
    import os
    # 去除首位空格
    path=path.strip()
    # 去除尾部 \ 符号
    path=path.rstrip("\\")

    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists=os.path.exists(path)

    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        print (path+' 创建成功')
        # 创建目录操作函数
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print (path+' 目录已存在')
        return False