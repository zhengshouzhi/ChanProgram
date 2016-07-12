 # -*- coding: utf-8 -*-
from DataInter import *
import matplotlib.pyplot as plt
import datetime
from time import strftime, localtime
from GenProcess import *
from DataProcess import *
#单均线多头评价
def MACD_MAL_Long_Comm(stockcode='000001',AnaCycle ='D',FilePath = 'FilePath',AvgLine = 5):
    FileName = stockcode + AnaCycle
    FilePath2 = FilePath + '\\'+FileName+ str(AvgLine) +'LongPerf.xls'
    FilePath = FilePath + '\\' + FileName + str(AvgLine)+'AvgLLong.xls'
    sheetname = 'DataAvgLine'
    MAL_BS = Get_TrdData_FromExcel(FilePath,sheetname)
    totalrows = len(MAL_BS)
    irows = 0
    staPrice = MAL_BS.loc[irows,'close']
    NetValue = 1
    NetIndValue = 1
    Perf_Stat = DataFrame([],columns = ['买入日期','卖出日期','买入价格',
                            '卖出价格','买卖盈亏','持有最大回辙','持有最高收益','持仓时间','净值','指数净值'])
    Perf_Stat_2 = DataFrame([],index=['盈利','亏损'],columns =
                       ['0-5','5-10','10-15','15-20','20-30','30-50','50-100','>100','总次数'])
    Perf_Stat_2.loc['盈利'] = 0
    Perf_Stat_2.loc['亏损'] = 0
    while(irows <totalrows):
        curOP = MAL_BS.loc[irows,'操作']
        if(curOP != '买入'):
            irows = irows + 1
        else:
            staPrice = MAL_BS.loc[irows,'close']
            break
    irows = 0
    while(irows < totalrows):
        dayCounter = 0
        MaxUP = 0
        MaxDown = 0
        BuyDate = 0
        SellDate = 0
        BSUPDown = 0
        BuyPrice = 0
        SellPrice = 0
        curOP = MAL_BS.loc[irows,'操作']
        if(curOP != '买入'):
            irows = irows + 1
        else:
            curUpDown = MAL_BS.loc[irows,'盈亏比例']
            MaxUP = curUpDown
            MaxDown = curUpDown
            BuyDate =  MAL_BS.loc[irows,'date']
            BuyPrice = MAL_BS.loc[irows,'close']
            irows = irows + 1
            while(irows < totalrows):
                curUpDown = MAL_BS.loc[irows,'盈亏比例']
                curOP = MAL_BS.loc[irows,'操作']
                if(curOP =='持股') :
                    dayCounter = dayCounter + 1
                    if(curUpDown > MaxUP):
                        MaxUP = curUpDown
                    if(curUpDown < MaxDown):
                        MaxDown = curUpDown
                    irows = irows + 1
                elif (curOP =='卖出'):
                    dayCounter = dayCounter + 1
                    if(curUpDown > MaxUP):
                        MaxUP = curUpDown
                    if(curUpDown < MaxDown):
                        MaxDown = curUpDown
                    SellDate = MAL_BS.loc[irows,'date']
                    SellPrice = MAL_BS.loc[irows,'close']
                    BSUPDown = curUpDown
                    Perf_Stat_2 = WinLoss_Stat(BSUPDown,Perf_Stat_2)
                    NetValue = NetValue * (1+curUpDown)
                    irows = irows + 1
                else:
                    break
            if(irows == totalrows):
                SellDate = MAL_BS.loc[totalrows-1,'date']
                SellPrice = MAL_BS.loc[totalrows-1,'close']
                BSUPDown = curUpDown
                NetValue = NetValue * (1+curUpDown)
                Perf_Stat_2 = WinLoss_Stat(BSUPDown,Perf_Stat_2)
            NetIndValue = SellPrice/staPrice
            s = Series([BuyDate,SellDate,BuyPrice,SellPrice,BSUPDown,MaxDown,MaxUP,dayCounter,NetValue,NetIndValue],index=
                ['买入日期','卖出日期','买入价格','卖出价格','买卖盈亏','持有最大回辙','持有最高收益','持仓时间','净值','指数净值'])
            Perf_Stat = Perf_Stat.append(s,ignore_index=True)
    sheetname1 = 'Perf'
    sheetname2 = 'PerfStat'
    writer = ExcelWriter(FilePath2)
    Perf_Stat.to_excel(writer,sheetname1)
    Perf_Stat_2.to_excel(writer,sheetname2)
    writer.save()
#业绩评价，单均线空头业绩评价
def MACD_MAL_Short_Comm(stockcode='000001',AnaCycle ='D',FilePath = 'FilePath',AvgLine='AvgLine'):
    FileName = stockcode + AnaCycle
    FilePath2 = FilePath + '\\'+FileName + str(AvgLine)+'ShortPerf.xls'
    FilePath = FilePath + '\\' + FileName +str(AvgLine)+'AvgLShort.xls'
    sheetname = 'DataAvgLine'
    MAL_BS = Get_TrdData_FromExcel(FilePath,sheetname)
    totalrows = len(MAL_BS)
    irows = 0
    staPrice = MAL_BS.loc[irows,'close']
    NetValue = 1
    NetIndValue = 1
    Perf_Stat = DataFrame([],columns = ['买入日期','卖出日期','买入价格',
                            '卖出价格','买卖盈亏','持有最大回辙','持有最高收益','持仓时间','净值','指数净值'])
    Perf_Stat_2 = DataFrame([],index=['盈利','亏损'],columns =
                       ['0-5','5-10','10-15','15-20','20-30','30-50','50-100','>100','总次数'])
    Perf_Stat_2.loc['盈利'] = 0
    Perf_Stat_2.loc['亏损'] = 0
    while(irows <totalrows):
        curOP = MAL_BS.loc[irows,'操作']
        if(curOP != '卖出'):
            irows = irows + 1
        else:
            staPrice = MAL_BS.loc[irows,'close']
            break
    irows = 0
    while(irows < totalrows):
        dayCounter = 0
        MaxUP = 0
        MaxDown = 0
        BuyDate = 0
        SellDate = 0
        BSUPDown = 0
        BuyPrice = 0
        SellPrice = 0
        curOP = MAL_BS.loc[irows,'操作']
        if(curOP != '卖出'):
            irows = irows + 1
        else:
            curUpDown = MAL_BS.loc[irows,'盈亏比例']
            MaxUP = curUpDown
            MaxDown = curUpDown
            BuyDate =  MAL_BS.loc[irows,'date']
            BuyPrice = MAL_BS.loc[irows,'close']
            irows = irows + 1
            while(irows < totalrows):
                curUpDown = MAL_BS.loc[irows,'盈亏比例']
                curOP = MAL_BS.loc[irows,'操作']
                if(curOP =='持币') :
                    dayCounter = dayCounter + 1
                    if(curUpDown > MaxUP):
                        MaxUP = curUpDown
                    if(curUpDown < MaxDown):
                        MaxDown = curUpDown
                    irows = irows + 1
                elif (curOP =='买入'):
                    dayCounter = dayCounter + 1
                    if(curUpDown > MaxUP):
                        MaxUP = curUpDown
                    if(curUpDown < MaxDown):
                        MaxDown = curUpDown
                    SellDate = MAL_BS.loc[irows,'date']
                    SellPrice = MAL_BS.loc[irows,'close']
                    BSUPDown = curUpDown
                    Perf_Stat_2 = WinLoss_Stat(BSUPDown,Perf_Stat_2)
                    NetValue = NetValue * (1+curUpDown)
                    irows = irows + 1
                else:
                    break
            if(irows == totalrows):
                SellDate = MAL_BS.loc[totalrows-1,'date']
                SellPrice = MAL_BS.loc[totalrows-1,'close']
                BSUPDown = curUpDown
                NetValue = NetValue * (1+curUpDown)
                Perf_Stat_2 = WinLoss_Stat(BSUPDown,Perf_Stat_2)
            NetIndValue = SellPrice/staPrice
            s = Series([BuyDate,SellDate,BuyPrice,SellPrice,BSUPDown,MaxDown,MaxUP,dayCounter,NetValue,NetIndValue],index=
                ['买入日期','卖出日期','买入价格','卖出价格','买卖盈亏','持有最大回辙','持有最高收益','持仓时间','净值','指数净值'])
            Perf_Stat = Perf_Stat.append(s,ignore_index=True)
    sheetname1 = 'Perf'
    sheetname2 = 'PerfStat'
    writer = ExcelWriter(FilePath2)
    Perf_Stat.to_excel(writer,sheetname1)
    Perf_Stat_2.to_excel(writer,sheetname2)
    writer.save()

#--------------------------------------------------------------------------------------------------------------------------------

#业绩评价，双均线,空头
def DouMACD_MAL_Short_Comm(stockcode='000001',AnaCycle ='D',FilePath = 'FilePath',AvgLShort = 5,AvgLLong = 10):
    FileName = stockcode + AnaCycle
    FilePath2 = FilePath + '\\'+FileName+str(AvgLShort)+'-'+str(AvgLLong) +'ShortPerf.xls'
    FilePath = FilePath + '\\' + FileName + str(AvgLShort)+'-'+str(AvgLLong) +'AvgLShort.xls'
    sheetname = 'DataAvgLine'
    MAL_BS = Get_TrdData_FromExcel(FilePath,sheetname)
    totalrows = len(MAL_BS)
    irows = 0
    staPrice = MAL_BS.loc[irows,'close']
    NetValue = 1
    NetIndValue = 1
    Perf_Stat = DataFrame([],columns = ['买入日期','卖出日期','买入价格',
                            '卖出价格','买卖盈亏','持有最大回辙','持有最高收益','持仓时间','净值','指数净值'])
    Perf_Stat_2 = DataFrame([],index=['盈利','亏损'],columns =
                       ['0-5','5-10','10-15','15-20','20-30','30-50','50-100','>100','总次数'])
    Perf_Stat_2.loc['盈利'] = 0
    Perf_Stat_2.loc['亏损'] = 0
    while(irows <totalrows):
        curOP = MAL_BS.loc[irows,'操作']
        if(curOP != '卖出'):
            irows = irows + 1
        else:
            staPrice = MAL_BS.loc[irows,'close']
            break
    irows = 0
    while(irows < totalrows):
        dayCounter = 0
        MaxUP = 0
        MaxDown = 0
        BuyDate = 0
        SellDate = 0
        BSUPDown = 0
        BuyPrice = 0
        SellPrice = 0
        curOP = MAL_BS.loc[irows,'操作']
        if(curOP != '卖出'):
            irows = irows + 1
        else:
            curUpDown = MAL_BS.loc[irows,'盈亏比例']
            MaxUP = curUpDown
            MaxDown = curUpDown
            BuyDate =  MAL_BS.loc[irows,'date']
            BuyPrice = MAL_BS.loc[irows,'close']
            irows = irows + 1
            while(irows < totalrows):
                curUpDown = MAL_BS.loc[irows,'盈亏比例']
                curOP = MAL_BS.loc[irows,'操作']
                if(curOP =='持币') :
                    dayCounter = dayCounter + 1
                    if(curUpDown > MaxUP):
                        MaxUP = curUpDown
                    if(curUpDown < MaxDown):
                        MaxDown = curUpDown
                    irows = irows + 1
                elif (curOP =='买入'):
                    dayCounter = dayCounter + 1
                    if(curUpDown > MaxUP):
                        MaxUP = curUpDown
                    if(curUpDown < MaxDown):
                        MaxDown = curUpDown
                    SellDate = MAL_BS.loc[irows,'date']
                    SellPrice = MAL_BS.loc[irows,'close']
                    BSUPDown = curUpDown
                    Perf_Stat_2 = WinLoss_Stat(BSUPDown,Perf_Stat_2)
                    NetValue = NetValue * (1+curUpDown)
                    irows = irows + 1
                else:
                    break
            if(irows == totalrows):
                SellDate = MAL_BS.loc[totalrows-1,'date']
                SellPrice = MAL_BS.loc[totalrows-1,'close']
                BSUPDown = curUpDown
                NetValue = NetValue * (1+curUpDown)
                Perf_Stat_2 = WinLoss_Stat(BSUPDown,Perf_Stat_2)
            NetIndValue = SellPrice/staPrice
            s = Series([BuyDate,SellDate,BuyPrice,SellPrice,BSUPDown,MaxDown,MaxUP,dayCounter,NetValue,NetIndValue],index=
                ['买入日期','卖出日期','买入价格','卖出价格','买卖盈亏','持有最大回辙','持有最高收益','持仓时间','净值','指数净值'])
            Perf_Stat = Perf_Stat.append(s,ignore_index=True)
    sheetname1 = 'Perf'
    sheetname2 = 'PerfStat'
    writer = ExcelWriter(FilePath2)
    Perf_Stat.to_excel(writer,sheetname1)
    Perf_Stat_2.to_excel(writer,sheetname2)
    writer.save()


#最简单黄白线上下穿法的业绩评价，应用于股票多头
#程序1：识别买卖、持有操作，并计算买入至卖出期间每一天的盈亏
def MACD_YWL_Long(stockcode='000001',AnaCycle ='D',FilePath = 'FilePath'):
    FileName = stockcode + AnaCycle
    FilePath2 = FilePath + '\\' + FileName +'MACDLong.xls'
    FilePath = FilePath + '\\' + FileName +'AvgLLong.xls'
    sheetname = 'MACDData'
    MACD_BS = Get_TrdData_FromExcel(FilePath,sheetname)
    MACD_BS['盈亏比例'] = 0
    totalrows = len(MACD_BS)
    irows = 0
    #找到第一个买入操作
    while(irows < totalrows):
        curOP = MACD_BS.loc[irows,'操作']
        if(curOP != '买入'):
            irows = irows + 1
        else:
            pricecost = MACD_BS.loc[irows,'close']
            irows = irows + 1
            while(irows < totalrows):
                curOP = MACD_BS.loc[irows,'操作']
                if(curOP =='持股') or (curOP =='卖出'):
                    curValue =  MACD_BS.loc[irows,'close']
                    WinLossPer = curValue/pricecost -1
                    MACD_BS.loc[irows,'盈亏比例'] = WinLossPer
                    irows = irows + 1
                else:
                    break
    Write_DF_T0_Excel(FilePath2,MACD_BS,sheetname)



#最简单黄白线上下穿法的业绩评价，应用于股票多头
#程序1：识别买卖、持有操作，并计算买入至卖出期间每一天的盈亏
def MACD_YWL_Long(stockcode='000001',AnaCycle ='D',FilePath = 'FilePath'):
    FileName = stockcode + AnaCycle
    FilePath2 = FilePath + '\\' + FileName +'MACDLong.xls'
    FilePath = FilePath + '\\' + FileName +'AvgLLong.xls'
    sheetname = 'MACDData'
    MACD_BS = Get_TrdData_FromExcel(FilePath,sheetname)
    MACD_BS['盈亏比例'] = 0
    totalrows = len(MACD_BS)
    irows = 0
    #找到第一个买入操作
    while(irows < totalrows):
        curOP = MACD_BS.loc[irows,'操作']
        if(curOP != '买入'):
            irows = irows + 1
        else:
            pricecost = MACD_BS.loc[irows,'close']
            irows = irows + 1
            while(irows < totalrows):
                curOP = MACD_BS.loc[irows,'操作']
                if(curOP =='持股') or (curOP =='卖出'):
                    curValue =  MACD_BS.loc[irows,'close']
                    WinLossPer = curValue/pricecost -1
                    MACD_BS.loc[irows,'盈亏比例'] = WinLossPer
                    irows = irows + 1
                else:
                    break
    Write_DF_T0_Excel(FilePath2,MACD_BS,sheetname)


#业绩评价，双均线多头的业绩评价
def DouMACD_MAL_Long_Comm(stockcode='000001',AnaCycle ='D',FilePath = 'FilePath',AvgLShort = 5,AvgLLong = 10):
    FileName = stockcode + AnaCycle
    FilePath2 = FilePath + '\\'+FileName+str(AvgLShort)+'-'+str(AvgLLong) +'LongPerf.xls'
    FilePath = FilePath + '\\' + FileName + str(AvgLShort)+'-'+str(AvgLLong) +'AvgLLong.xls'
    sheetname = 'DataAvgLine'
    MAL_BS = Get_TrdData_FromExcel(FilePath,sheetname)
    totalrows = len(MAL_BS)
    irows = 0
    staPrice = MAL_BS.loc[irows,'close']
    NetValue = 1
    NetIndValue = 1
    Perf_Stat = DataFrame([],columns = ['买入日期','卖出日期','买入价格',
                            '卖出价格','买卖盈亏','持有最大回辙','持有最高收益','持仓时间','净值','指数净值'])
    Perf_Stat_2 = DataFrame([],index=['盈利','亏损'],columns =
                       ['0-5','5-10','10-15','15-20','20-30','30-50','50-100','>100','总次数'])
    Perf_Stat_2.loc['盈利'] = 0
    Perf_Stat_2.loc['亏损'] = 0
    while(irows <totalrows):
        curOP = MAL_BS.loc[irows,'操作']
        if(curOP != '买入'):
            irows = irows + 1
        else:
            staPrice = MAL_BS.loc[irows,'close']
            break
    irows = 0
    while(irows < totalrows):
        dayCounter = 0
        MaxUP = 0
        MaxDown = 0
        BuyDate = 0
        SellDate = 0
        BSUPDown = 0
        BuyPrice = 0
        SellPrice = 0
        curOP = MAL_BS.loc[irows,'操作']
        if(curOP != '买入'):
            irows = irows + 1
        else:
            curUpDown = MAL_BS.loc[irows,'盈亏比例']
            MaxUP = curUpDown
            MaxDown = curUpDown
            BuyDate =  MAL_BS.loc[irows,'date']
            BuyPrice = MAL_BS.loc[irows,'close']
            irows = irows + 1
            while(irows < totalrows):
                curUpDown = MAL_BS.loc[irows,'盈亏比例']
                curOP = MAL_BS.loc[irows,'操作']
                if(curOP =='持股') :
                    dayCounter = dayCounter + 1
                    if(curUpDown > MaxUP):
                        MaxUP = curUpDown
                    if(curUpDown < MaxDown):
                        MaxDown = curUpDown
                    irows = irows + 1
                elif (curOP =='卖出'):
                    dayCounter = dayCounter + 1
                    if(curUpDown > MaxUP):
                        MaxUP = curUpDown
                    if(curUpDown < MaxDown):
                        MaxDown = curUpDown
                    SellDate = MAL_BS.loc[irows,'date']
                    SellPrice = MAL_BS.loc[irows,'close']
                    BSUPDown = curUpDown
                    Perf_Stat_2 = WinLoss_Stat(BSUPDown,Perf_Stat_2)
                    NetValue = NetValue * (1+curUpDown)
                    irows = irows + 1
                else:
                    break
            if(irows == totalrows):
                SellDate = MAL_BS.loc[totalrows-1,'date']
                SellPrice = MAL_BS.loc[totalrows-1,'close']
                BSUPDown = curUpDown
                NetValue = NetValue * (1+curUpDown)
                Perf_Stat_2 = WinLoss_Stat(BSUPDown,Perf_Stat_2)
            NetIndValue = SellPrice/staPrice
            s = Series([BuyDate,SellDate,BuyPrice,SellPrice,BSUPDown,MaxDown,MaxUP,dayCounter,NetValue,NetIndValue],index=
                ['买入日期','卖出日期','买入价格','卖出价格','买卖盈亏','持有最大回辙','持有最高收益','持仓时间','净值','指数净值'])
            Perf_Stat = Perf_Stat.append(s,ignore_index=True)
    sheetname1 = 'Perf'
    sheetname2 = 'PerfStat'
    writer = ExcelWriter(FilePath2)
    Perf_Stat.to_excel(writer,sheetname1)
    Perf_Stat_2.to_excel(writer,sheetname2)
    writer.save()


#业绩评价，股标多头把结果存到文件中：
def MACD_YWL_Long_Comm(stockcode='000001',AnaCycle ='D',FilePath = 'FilePath'):
    FileName = stockcode + AnaCycle
    FilePath2 = FilePath + '\\'+FileName + 'LongPerf.xls'
    FilePath = FilePath + '\\' + FileName +'MACDLong.xls'
    sheetname = 'MACDData'
    MACD_BS = Get_TrdData_FromExcel(FilePath,sheetname)
    totalrows = len(MACD_BS)
    irows = 0
    staPrice = MACD_BS.loc[irows,'close']
    NetValue = 1
    NetIndValue = 1
    Perf_Stat = DataFrame([],columns = ['买入日期','卖出日期','买入价格',
                            '卖出价格','买卖盈亏','持有最大回辙','持有最高收益','持仓时间','净值','指数净值'])
    Perf_Stat_2 = DataFrame([],index=['盈利','亏损'],columns =
                       ['0-5','5-10','10-15','15-20','20-30','30-50','50-100','>100','总次数'])
    Perf_Stat_2.loc['盈利'] = 0
    Perf_Stat_2.loc['亏损'] = 0
    while(irows <totalrows):
        curOP = MACD_BS.loc[irows,'操作']
        if(curOP != '买入'):
            irows = irows + 1
        else:
            staPrice = MACD_BS.loc[irows,'close']
            break
    irows = 0
    while(irows < totalrows):
        dayCounter = 0
        MaxUP = 0
        MaxDown = 0
        BuyDate = 0
        SellDate = 0
        BSUPDown = 0
        BuyPrice = 0
        SellPrice = 0
        curOP = MACD_BS.loc[irows,'操作']
        if(curOP != '买入'):
            irows = irows + 1
        else:
            curUpDown = MACD_BS.loc[irows,'盈亏比例']
            MaxUP = curUpDown
            MaxDown = curUpDown
            BuyDate =  MACD_BS.loc[irows,'date']
            BuyPrice = MACD_BS.loc[irows,'close']
            irows = irows + 1
            while(irows < totalrows):
                curUpDown = MACD_BS.loc[irows,'盈亏比例']
                curOP = MACD_BS.loc[irows,'操作']
                if(curOP =='持股') :
                    dayCounter = dayCounter + 1
                    if(curUpDown > MaxUP):
                        MaxUP = curUpDown
                    if(curUpDown < MaxDown):
                        MaxDown = curUpDown
                    irows = irows + 1
                elif (curOP =='卖出'):
                    dayCounter = dayCounter + 1
                    if(curUpDown > MaxUP):
                        MaxUP = curUpDown
                    if(curUpDown < MaxDown):
                        MaxDown = curUpDown
                    SellDate = MACD_BS.loc[irows,'date']
                    SellPrice = MACD_BS.loc[irows,'close']
                    BSUPDown = curUpDown
                    Perf_Stat_2 = WinLoss_Stat(BSUPDown,Perf_Stat_2)
                    NetValue = NetValue * (1+curUpDown)
                    irows = irows + 1
                else:
                    break
            if(irows == totalrows):
                SellDate = MACD_BS.loc[totalrows-1,'date']
                SellPrice = MACD_BS.loc[totalrows-1,'close']
                BSUPDown = curUpDown
                NetValue = NetValue * (1+curUpDown)
                Perf_Stat_2 = WinLoss_Stat(BSUPDown,Perf_Stat_2)
            NetIndValue = SellPrice/staPrice
            s = Series([BuyDate,SellDate,BuyPrice,SellPrice,BSUPDown,MaxDown,MaxUP,dayCounter,NetValue,NetIndValue],index=
                ['买入日期','卖出日期','买入价格','卖出价格','买卖盈亏','持有最大回辙','持有最高收益','持仓时间','净值','指数净值'])
            Perf_Stat = Perf_Stat.append(s,ignore_index=True)
    sheetname1 = 'Perf'
    sheetname2 = 'PerfStat'
    writer = ExcelWriter(FilePath2)
    Perf_Stat.to_excel(writer,sheetname1)
    Perf_Stat_2.to_excel(writer,sheetname2)
    writer.save()


#最简单黄白线上下穿法的业绩评价，应用于期指空头
#识别买卖、持有操作，并计算卖出（开仓）至买入（平仓）期间每一天的盈亏
def MACD_YWL_Short(stockcode='000001',AnaCycle ='D',FilePath = 'FilePath'):
    FileName = stockcode + AnaCycle
    FilePath2 = FilePath + '\\' + FileName +'MACDShort.xls'
    FilePath = FilePath + '\\' + FileName +'MACD.xls'
    sheetname = 'MACDData'
    MACD_BS = Get_TrdData_FromExcel(FilePath,sheetname)
    MACD_BS['盈亏比例'] = 0
    totalrows = len(MACD_BS)
    irows = 0
    #找到第一个卖出操作
    while(irows < totalrows):
        curOP = MACD_BS.loc[irows,'操作']
        if(curOP != '卖出'):
            irows = irows + 1
        else:
            pricecost = MACD_BS.loc[irows,'close']
            irows = irows + 1
            while(irows < totalrows):
                curOP = MACD_BS.loc[irows,'操作']
                if(curOP =='持币') or (curOP =='买入'):
                    curValue =  MACD_BS.loc[irows,'close']
                    WinLossPer = (pricecost-curValue)/pricecost
                    MACD_BS.loc[irows,'盈亏比例'] = WinLossPer
                    irows = irows + 1
                else:
                    break
    Write_DF_T0_Excel(FilePath2,MACD_BS,sheetname)

#业绩评价，股标空头把结果存到文件中：
def MACD_YWL_Short_Comm(stockcode='000001',AnaCycle ='D',FilePath = 'FilePath'):
    FileName = stockcode + AnaCycle
    FilePath2 = FilePath + '\\'+FileName + 'ShortPerf.xls'
    FilePath = FilePath + '\\' + FileName +'MACDShort.xls'
    sheetname = 'MACDData'
    MACD_BS = Get_TrdData_FromExcel(FilePath,sheetname)
    totalrows = len(MACD_BS)
    irows = 0
    staPrice = MACD_BS.loc[irows,'close']
    NetValue = 1
    NetIndValue = 1
    Perf_Stat = DataFrame([],columns = ['买入日期','卖出日期','买入价格',
                            '卖出价格','买卖盈亏','持有最大回辙','持有最高收益','持仓时间','净值','指数净值'])
    Perf_Stat_2 = DataFrame([],index=['盈利','亏损'],columns =
                       ['0-5','5-10','10-15','15-20','20-30','30-50','50-100','>100','总次数'])
    Perf_Stat_2.loc['盈利'] = 0
    Perf_Stat_2.loc['亏损'] = 0
    while(irows <totalrows):
        curOP = MACD_BS.loc[irows,'操作']
        if(curOP != '卖出'):
            irows = irows + 1
        else:
            staPrice = MACD_BS.loc[irows,'close']
            break
    irows = 0
    while(irows < totalrows):
        dayCounter = 0
        MaxUP = 0
        MaxDown = 0
        BuyDate = 0
        SellDate = 0
        BSUPDown = 0
        BuyPrice = 0
        SellPrice = 0
        curOP = MACD_BS.loc[irows,'操作']
        if(curOP != '卖出'):
            irows = irows + 1
        else:
            curUpDown = MACD_BS.loc[irows,'盈亏比例']
            MaxUP = curUpDown
            MaxDown = curUpDown
            BuyDate =  MACD_BS.loc[irows,'date']
            BuyPrice = MACD_BS.loc[irows,'close']
            irows = irows + 1
            while(irows < totalrows):
                curUpDown = MACD_BS.loc[irows,'盈亏比例']
                curOP = MACD_BS.loc[irows,'操作']
                if(curOP =='持币') :
                    dayCounter = dayCounter + 1
                    if(curUpDown > MaxUP):
                        MaxUP = curUpDown
                    if(curUpDown < MaxDown):
                        MaxDown = curUpDown
                    irows = irows + 1
                elif (curOP =='买入'):
                    dayCounter = dayCounter + 1
                    if(curUpDown > MaxUP):
                        MaxUP = curUpDown
                    if(curUpDown < MaxDown):
                        MaxDown = curUpDown
                    SellDate = MACD_BS.loc[irows,'date']
                    SellPrice = MACD_BS.loc[irows,'close']
                    BSUPDown = curUpDown
                    Perf_Stat_2 = WinLoss_Stat(BSUPDown,Perf_Stat_2)
                    NetValue = NetValue * (1+curUpDown)
                    irows = irows + 1
                else:
                    break
            if(irows == totalrows):
                SellDate = MACD_BS.loc[totalrows-1,'date']
                SellPrice = MACD_BS.loc[totalrows-1,'close']
                BSUPDown = curUpDown
                NetValue = NetValue * (1+curUpDown)
                Perf_Stat_2 = WinLoss_Stat(BSUPDown,Perf_Stat_2)
            NetIndValue = SellPrice/staPrice
            s = Series([BuyDate,SellDate,BuyPrice,SellPrice,BSUPDown,MaxDown,MaxUP,dayCounter,NetValue,NetIndValue],index=
                ['买入日期','卖出日期','买入价格','卖出价格','买卖盈亏','持有最大回辙','持有最高收益','持仓时间','净值','指数净值'])
            Perf_Stat = Perf_Stat.append(s,ignore_index=True)
    sheetname1 = 'Perf'
    sheetname2 = 'PerfStat'
    writer = ExcelWriter(FilePath2)
    Perf_Stat.to_excel(writer,sheetname1)
    Perf_Stat_2.to_excel(writer,sheetname2)
    writer.save()

