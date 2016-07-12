 # -*- coding: utf-8 -*-
from DataInter import *
import matplotlib.pyplot as plt
import datetime
from time import strftime, localtime
from GenProcess import *
from DataProcess import *
#统计在衰退、蛰伏、伪装、绿灯状态下的涨跌次数以及幅度，混沌交易法的实证
def MFITrendStat(StockCode = 'sh',AnaCycle = 'D'):
    S_Trd_Data = Get_TrData_FromTs (StockCode,AnaCycle)
    S_Trd_Data = Data_MFI(S_Trd_Data)
    totalrows = len(S_Trd_Data)
    irows = 1
    #ST衰退，ZF蛰伏，WZ伪装，LD绿灯
    STCounter = 0
    ZFCounter = 0
    WZCounter = 0
    LDCounter = 0
    totalST = 0
    totalZF = 0
    totalWZ = 0
    totalLD = 0
    while(irows < totalrows):
        curMFIStatus = S_Trd_Data.loc[irows,'MTIStatus']
        curRiseDown = S_Trd_Data.loc[irows,'updown']
        if (curMFIStatus =='衰退'):
            STCounter = STCounter + 1
            totalST = totalST +abs(curRiseDown)
        elif (curMFIStatus =='蛰伏'):
            ZFCounter = ZFCounter + 1
            totalZF = totalZF +abs(curRiseDown)
        elif (curMFIStatus =='伪装'):
            WZCounter = WZCounter + 1
            totalWZ = totalWZ +abs(curRiseDown)
        elif(curMFIStatus =='绿灯'):
            LDCounter = LDCounter + 1
            totalLD = totalLD +abs(curRiseDown)
        irows = irows + 1
    avgST = totalST/STCounter*100
    avgZF = totalZF/ZFCounter*100
    avgWZ = totalWZ/WZCounter*100
    avgLD = totalLD/LDCounter*100
    print('衰退',STCounter,avgST)
    print('蛰伏',ZFCounter,avgZF)
    print('伪装',WZCounter,avgWZ)
    print('绿灯',LDCounter,avgLD)


#对证券交易记录进行业绩归因,此程序主要考虑各股的操作频次以及操作的盈亏，包括个股盈亏，个股持仓时间，按月统计的加减仓时机
def OpeComment(FileFolder = 'FileFolder',ProductName = 'ProductName',Worksheet = 'Worksheet'):
    OriFilePath = FileFolder + '\\'+ProductName +'.xls'
    try:
        Oper_Data = pd.read_excel(io=OriFilePath,sheetname = Worksheet)
    except Exception as err:
        print (str(err))
    Oper_Data = StockCode_Stand(Oper_Data)
    Oper_Data = Oper_Data.sort_values(by=['证券代码','成交日期','买卖标志'],ascending=[True,True,True])
    Oper_Data = DataFrame(Oper_Data.values,columns=Oper_Data.columns)
    FilePath1 = FileFolder + '\\'+ProductName+'\\'+'代码排序.xls'
    Write_DF_T0_Excel(FilePath1,Oper_Data)
    Oper_Data = MergeSameDayOpe(Oper_Data)
    Oper_Data = DataFrame(Oper_Data.values,columns=Oper_Data.columns)
    #股票的操作频率
    holdPeriod = Oper_Freq(Oper_Data)
    FilePath6 = FileFolder + '\\'+ProductName+'\\'+'操作频率.xls'
    Write_STo_Excel (FilePath6 ,holdPeriod,sheetname = '操作频率')
    FilePath3 = FileFolder + '\\'+ProductName+'\\'+'日内合并.xls'
    Write_DF_T0_Excel(FilePath3,Oper_Data)
    FilePath2 = FileFolder + '\\'+ProductName+'\\'+'操作次数.xls'
    df_OperCounter = OperCounter(Oper_Data,FilePath2)
    df_OperTiming = Op_byMonth(Oper_Data)
    FilePath4 = FileFolder + '\\'+ProductName+'\\'+'操作时机.xls'
    Write_DF_T0_Excel(FilePath4,df_OperTiming)
    Oper_Data = Oper_Data.sort_values(by='成交日期',ascending=True)
    Oper_Data = DataFrame(Oper_Data.values,columns=Oper_Data.columns)
    FilePath5 = FileFolder + '\\'+ProductName+'\\'+'时机日内合并.xls'
    Write_DF_T0_Excel(FilePath5,Oper_Data)
    return df_OperTiming
#统计股票的操作频率，统计股票的平均持有时间
def Oper_Freq(Oper_Data='Oper_Data'):
    holdPeriod = Series([0,0,0,0,0,0,0],index =['1','2-5','6-15','16-60','61-120','121-240','>240'])
    totalrows = len(Oper_Data)
    irows = 0
    #listbuy和listsell用于存储同一股票在周期内的买卖操作
    listbuy = []
    listsell = []
    prestockcode = Oper_Data.loc[irows,'证券代码']
    preOper = Oper_Data.loc[irows,'买卖标志']
    preOperDate = Oper_Data.loc[irows,'成交日期']
    if(preOper == '证券买入'):
        listbuy.append(preOperDate)
    elif(preOper == '证券卖出'):
        listsell.append(preOperDate)
    irows = irows + 1
    #对所有交易数据进行循环处理
    while (irows < totalrows-1):
        curstockcode = Oper_Data.loc[irows,'证券代码']
        curOper = Oper_Data.loc[irows,'买卖标志']
        curOperDate = Oper_Data.loc[irows,'成交日期']
        while(curstockcode == prestockcode) and(irows < totalrows) :
            if(curOper == '证券买入'):
                listbuy.append(curOperDate)
            elif(curOper == '证券卖出'):
                listsell.append(curOperDate)
            irows = irows + 1
            if(irows < totalrows ):
                curstockcode = Oper_Data.loc[irows,'证券代码']
                curOper = Oper_Data.loc[irows,'买卖标志']
                curOperDate = Oper_Data.loc[irows,'成交日期']
        buylen = len(listbuy)
        selllen = len(listsell)
        if(buylen != 0) and (selllen != 0):
            if(buylen > selllen):
                i = 0
                fillvalue = listsell[selllen-1]
                while(i<(buylen-selllen)):
                    listsell.append(fillvalue)
                    i = i + 1
            elif(buylen < selllen):
                i = 0
                fillvalue = listbuy[buylen-1]
                while(i<(selllen-buylen)):
                    listbuy.append(fillvalue)
                    i = i + 1
            stockcode = codeType(prestockcode)
            SourceData = Get_TrData_FromTs(stockcode,AnaCycle='D')
            totaltick = len(listbuy)
            iIndex = 0
            while (iIndex < totaltick):
                startdate = listbuy[iIndex]
                enddate = listsell[iIndex]
                startdate = str(flo_to_Date(startdate))
                enddate = str(flo_to_Date(enddate))
                trd_days = trdCount(SourceData,startdate,enddate)
                if(trd_days == 1):
                    holdPeriod['1'] = holdPeriod['1'] +1
                elif(trd_days > 1) and (trd_days <= 5):
                     holdPeriod['2-5'] = holdPeriod['2-5'] +1
                elif(trd_days > 5) and (trd_days <= 15):
                     holdPeriod['6-15'] = holdPeriod['6-15'] +1
                elif(trd_days > 15) and (trd_days <= 60):
                     holdPeriod['16-60'] = holdPeriod['16-60'] +1
                elif(trd_days > 60) and (trd_days <= 120):
                     holdPeriod['61-120'] = holdPeriod['61-120'] +1
                elif(trd_days > 120) and (trd_days <= 240):
                     holdPeriod['121-240'] = holdPeriod['121-240'] +1
                iIndex = iIndex + 1
        listbuy = []
        listsell = []
        prestockcode = curstockcode
        preOper = curOper
        preOperDate = curOperDate
        if(preOper == '证券买入'):
            listbuy.append(preOperDate)
        elif(preOper == '证券卖出'):
            listsell.append(preOperDate)
        irows = irows + 1
    return  holdPeriod

#按月统计买入总量、卖出总量，以判断产品的买卖时机把握能力。
def Op_byMonth(Oper_Data='Oper_Data'):
    Oper_Data = Oper_Data.sort_values(by='成交日期',ascending = True)
    df_OperTiming = DataFrame([],columns = ['年','月','证券买入','证券卖出','净买入量(万元)','融券','定价申购'])
    Oper_Data = DataFrame(Oper_Data.values,columns=Oper_Data.columns)
    totalrows = len(Oper_Data)
    irows = 0
    Date = Oper_Data.loc[irows,'成交日期']
    dt = flo_to_Date(Date)
    preyear = dt.year
    premonth = dt.month
    buyVolume = 0
    buyAmount = 0
    sellVolume = 0
    sellAmount = 0
    rqVolume = 0
    rqAmount = 0
    sgVolume = 0
    sgAmount = 0
    preOper = Oper_Data.loc[irows,'买卖标志']
    preVolume = Oper_Data.loc[irows,'成交数量']
    preAmount = Oper_Data.loc[irows,'成交金额']
    if(preOper =='证券买入'):
        buyVolume = preVolume
        buyAmount = preAmount
    elif(preOper == '证券卖出'):
        sellVolume = preVolume
        sellAmount = preAmount
    elif(preOper == '融券'):
        rqVolume = preVolume
        rqAmount = preAmount
    elif(preOper == '定价申购'):
        sgVolume = preVolume
        sgAmount = preAmount
    irows = irows + 1
    while(irows < totalrows):
        Date = Oper_Data.loc[irows,'成交日期']
        dt = flo_to_Date(Date)
        curyear = dt.year
        curmonth = dt.month
        while (curyear == preyear) and (curmonth == premonth) and (irows < totalrows ):
            curOper = Oper_Data.loc[irows,'买卖标志']
            curVolume = Oper_Data.loc[irows,'成交数量']
            curAmount = Oper_Data.loc[irows,'成交金额']
            if(curOper =='证券买入'):
                buyVolume = buyVolume + curVolume
                buyAmount = buyAmount + curAmount
            elif(curOper == '证券卖出'):
                sellVolume = sellVolume + curVolume
                sellAmount = sellAmount + curAmount
            elif(curOper == '融券'):
                rqVolume = rqVolume + curVolume
                rqAmount = rqAmount + curAmount
            elif(curOper == '定价申购'):
                sgVolume = sgVolume + curVolume
                sgAmount = sgAmount + curAmount
            irows = irows + 1
            if(irows < totalrows):
                Date = Oper_Data.loc[irows,'成交日期']
                dt = flo_to_Date(Date)
                curyear = dt.year
                curmonth = dt.month
        s = Series ([2015,1,0,0,0,0,0],index = ['年','月','证券买入','证券卖出','净买入量(万元)','融券','定价申购'])
        s['年'] = preyear
        s['月'] = premonth
        s['证券买入'] = buyAmount
        s['证券卖出'] = sellAmount
        s['净买入量(万元)'] = (buyAmount -sellAmount)/10000
        s['融券'] = rqAmount
        s['定价申购'] = sgAmount
        df_OperTiming = df_OperTiming.append(s,ignore_index=True)
        if(irows < totalrows):
            preyear = curyear
            premonth = curmonth
            buyVolume = 0
            buyAmount = 0
            sellVolume = 0
            sellAmount = 0
            rqVolume = 0
            rqAmount = 0
            sgVolume = 0
            sgAmount = 0
            preOper = Oper_Data.loc[irows,'买卖标志']
            preVolume = Oper_Data.loc[irows,'成交数量']
            preAmount = Oper_Data.loc[irows,'成交金额']
            if(preOper =='证券买入'):
                buyVolume = preVolume
                buyAmount = preAmount
            elif(preOper == '证券卖出'):
                sellVolume = preVolume
                sellAmount = preAmount
            elif(preOper == '融券'):
                rqVolume = preVolume
                rqAmount = preAmount
            elif(preOper == '定价申购'):
                sgVolume = preVolume
                sgAmount = preAmount
            irows = irows + 1
        else:
            break
    return df_OperTiming

#将证券代码统一为codeType类型，以解决‘sh600001’或深市的‘0’被Excel自动去除的问题
def StockCode_Stand(Oper_Data='Oper_Data'):
    totalrows = len(Oper_Data)
    irows = 0
    while(irows < totalrows):
        StockCode = Oper_Data.loc[irows,'证券代码']
        Oper_Data.loc[irows,'证券代码'] = codeType(StockCode)
        irows = irows + 1
    return Oper_Data

#统计个股的操作总次数（一天内对同一支股票的买卖算一次操作），买入卖出次数
def OperCounter(Oper_Data='Oper_Data',FilePath='FilePath'):
    opeCounter = 1
    buyCounter = 0
    sellCounter = 0
    buyVolume = 0
    sellVolume = 0
    buyAmount = 0
    sellAmount = 0
    IsFirst = True
    df_OperCounter = DataFrame([],columns = ['证券代码','操作次数','证券名称',
            '买入次数','卖出次数','买入数量','卖出数量','买入总额(万元)','卖出总额(万元)'])
    totalrows = len(Oper_Data)

    irows = 0
    preStockCode = codeType(Oper_Data.loc[irows,'证券代码'])
    curStockOpe = Oper_Data.loc[irows,'买卖标志']
    if(curStockOpe == '证券买入'):
        buyCounter = buyCounter + 1
        buyVolume = buyVolume + Oper_Data.loc[irows,'成交数量']
        curAmount = Oper_Data.loc[irows,'成交金额']
        buyAmount = buyAmount + curAmount
    elif(curStockOpe == '证券卖出'):
        sellCounter = sellCounter + 1
        sellVolume = sellVolume + Oper_Data.loc[irows,'成交数量']
        curAmount = Oper_Data.loc[irows,'成交金额']
        sellAmount = sellAmount + curAmount
    irows = irows + 1
    while(irows < totalrows):
        opeCounter = 1
        curStockCode = codeType(Oper_Data.loc[irows,'证券代码'])
        while(curStockCode == preStockCode) :
            curStockOpe = Oper_Data.loc[irows,'买卖标志']
            opeCounter = opeCounter + 1
            if(curStockOpe == '证券买入'):
                buyCounter = buyCounter + 1
                buyVolume = buyVolume + Oper_Data.loc[irows,'成交数量']
                curAmount = Oper_Data.loc[irows,'成交金额']
                buyAmount = buyAmount + curAmount
            elif(curStockOpe == '证券卖出'):
                sellCounter = sellCounter + 1
                sellVolume = sellVolume + Oper_Data.loc[irows,'成交数量']
                curAmount = Oper_Data.loc[irows,'成交金额']
                sellAmount = sellAmount + curAmount
            irows = irows + 1
            if(irows <totalrows):
                curStockCode = codeType(Oper_Data.loc[irows,'证券代码'])
            else:
                break
        preStockName = Oper_Data.loc[irows-1,'证券名称']
        buyAmount = buyAmount/10000
        sellAmount = sellAmount/10000
        s = Series([preStockCode,opeCounter,preStockName,buyCounter,sellCounter,buyVolume,sellVolume,buyAmount,sellAmount],
            index=['证券代码','操作次数','证券名称','买入次数','卖出次数','买入数量','卖出数量',
                   '买入总额(万元)','卖出总额(万元)'])
        df_OperCounter = df_OperCounter.append(s.T,ignore_index=True)
        preStockCode = curStockCode
        buyCounter = 0
        sellCounter = 0
        buyVolume = 0
        sellVolume = 0
        buyAmount = 0
        sellAmount = 0
        if(irows < totalrows):
            curStockOpe = Oper_Data.loc[irows,'买卖标志']
            if(curStockOpe == '证券买入'):
                buyCounter = buyCounter + 1
                buyVolume = buyVolume + Oper_Data.loc[irows,'成交数量']
                curAmount = Oper_Data.loc[irows,'成交金额']
                buyAmount = buyAmount + curAmount
            elif(curStockOpe == '证券卖出'):
                sellCounter = sellCounter + 1
                sellVolume = sellVolume + Oper_Data.loc[irows,'成交数量']
                curAmount = Oper_Data.loc[irows,'成交金额']
                sellAmount = sellAmount + curAmount
        irows = irows + 1
    df_OperCounter = df_OperCounter.sort_values(by='买入总额(万元)',ascending=False)
    df_OperCounter = DataFrame(df_OperCounter.values,columns = df_OperCounter.columns)
    df_OperCounter = OperWinLoss(df_OperCounter)
    Write_DF_T0_Excel(FilePath,df_OperCounter)

#在各股的买入卖出列中，加上买入均价、卖出均价，卖出盈亏，现价（收盘），持仓盈亏,盈亏包括金额（万元），比例
def OperWinLoss( df_OperCounter = 'df_OperCounter'):
    df_OperCounter['买入均价'] = None
    df_OperCounter['卖出均价'] = None
    df_OperCounter['净买入量(万股)'] = None
    df_OperCounter['盈亏比例'] = None
    df_OperCounter['卖出盈亏'] = None
    df_OperCounter['最新收盘'] = None
    df_OperCounter['持仓盈亏'] = None
    totalrows = len(df_OperCounter)
    irows = 0
    while(irows < totalrows):
        buyVolume = df_OperCounter.loc[irows,'买入数量']
        sellVolume = df_OperCounter.loc[irows,'卖出数量']
        buyAmount = df_OperCounter.loc[irows,'买入总额(万元)']
        sellAmount = df_OperCounter.loc[irows,'卖出总额(万元)']
        netBuy = buyVolume - sellVolume
        if(buyVolume != 0):
            avgBuy = buyAmount/buyVolume
            df_OperCounter.loc[irows,'买入均价'] = avgBuy
        else:
            avgBuy = 0
            df_OperCounter.loc[irows,'买入均价'] = avgBuy
        if(sellVolume!=0):
            avgSell = sellAmount/sellVolume
            df_OperCounter.loc[irows,'卖出均价'] = avgSell
        else:
            avgSell = 0
            df_OperCounter.loc[irows,'卖出均价'] = avgSell
        if(avgBuy != 0) and (avgSell != 0):
            WinLossPer = avgSell/avgBuy -1
        else:
            WinLossPer = 0
        df_OperCounter.loc[irows,'盈亏比例'] = WinLossPer
        df_OperCounter.loc[irows,'净买入量(万股)'] = netBuy/10000
        netWinLoss = sellAmount *WinLossPer/(1+WinLossPer)
        df_OperCounter.loc[irows,'卖出盈亏'] = netWinLoss
        stockCode = df_OperCounter.loc[irows,'证券代码']
        if(netBuy != 0):
            latestClose = Latest_Close(stockCode,'D')
            df_OperCounter.loc[irows,'最新收盘'] = latestClose
            holdWinLoss = netBuy *(latestClose -avgBuy )
            df_OperCounter.loc[irows,'持仓盈亏'] = holdWinLoss
        irows = irows + 1
    return df_OperCounter
#合并同一天，同一支股票的同向操作
def Merge_Series(preRec='preRec',curRec='curRec'):
    totalVolume = preRec['成交数量'] + curRec['成交数量']
    totalAmount = preRec['成交金额'] + curRec['成交金额']
    avgPrice = totalAmount/totalVolume
    preRec['成交数量'] = totalVolume
    preRec['成交金额'] = totalAmount
    preRec['成交价格'] = avgPrice
    return preRec

#合并交易记录中同一天操作的同一支股票同一天的交易
def MergeSameDayOpe(Oper_Data='Oper_Data'):
    Oper_Data = Oper_Data[['成交日期','证券代码','证券名称','买卖标志','成交价格','成交数量','成交金额']]
    totalrows = len(Oper_Data)
    irows = 0
    Mer_Ope_Data = DataFrame([],columns=Oper_Data.columns)
    preRec = Oper_Data.iloc[irows]
    irows = irows +1
    while(irows < totalrows):
        curRec = Oper_Data.iloc[irows]
        preDate = preRec['成交日期']
        curDate = curRec['成交日期']
        preCode = preRec['证券代码']
        curCode = curRec['证券代码']
        preOper = preRec['买卖标志']
        curOper = curRec['买卖标志']
        if (preDate ==curDate) and (preCode ==curCode)and(preOper == curOper):
            preRec = Merge_Series(preRec,curRec)
        else:
            Mer_Ope_Data =Mer_Ope_Data.append(preRec)
            preRec = curRec
        irows = irows + 1
    return Mer_Ope_Data








