# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from DataProcess import *
from DataInter import *
from DataPlot import *
import datetime
from GenProcess import *
from MAMACDProcess import *
import pandas as pd
#单均线策略相关函数
#计算收盘价与均线的上下关系，单均线函数1
def MVAg_WZ(stockcode='000001',AnaCycle ='D',FilePath = 'FilePath',AvgLine = 5):
    Avgl = str(AvgLine)
    FilePath2 = FilePath + '\\'+ stockcode + AnaCycle +Avgl +'.xls'
    FilePath = FilePath + '\\'+ stockcode + AnaCycle + '.xls'
    sheetname ='OriData'
    Trd_Data = Get_TrdData_FromExcel(FilePath,sheetname)
    Trd_Data = Data_Avg_Line(Trd_Data,AvgLine)
    Trd_Data['位置关系'] = '无'
    irows = 0
    totalrows = len(Trd_Data)
    Avgline = 'Avg'+str(Avgl)
    while(irows < totalrows):
        curClose = Trd_Data.loc[irows,'close']
        AvgPrice = Trd_Data.loc[irows,Avgline]
        if(curClose!='无') and (AvgPrice!='无'):
            Gap = curClose - AvgPrice
            if(Gap > 0):
                Trd_Data.loc[irows,'位置关系'] = '上'
            elif(Gap < 0):
                Trd_Data.loc[irows,'位置关系'] = '下'
        irows = irows + 1
    writer = ExcelWriter(FilePath2)
    Trd_Data.to_excel(writer,'DataAvgLine')
    writer.save()
    return Trd_Data

def MVAg_WZ_Dir(stockcode='000001',AnaCycle ='D',FilePath = 'FilePath',AvgLine = 5):
    Avgl = str(AvgLine)
    FilePath2 = FilePath + '\\'+ stockcode + AnaCycle +Avgl +'.xls'
    FilePath = FilePath + '\\'+ stockcode + AnaCycle + '.xls'
    sheetname ='OriData'
    Trd_Data = Get_TrdData_FromExcel(FilePath,sheetname)
    Trd_Data = Data_Avg_Line(Trd_Data,AvgLine)
    Trd_Data['位置关系'] = '无'
    irows = 0
    totalrows = len(Trd_Data)
    Avgline = 'Avg'+str(Avgl)
    while(irows < totalrows):
        curClose = Trd_Data.loc[irows,'close']
        AvgPrice = Trd_Data.loc[irows,Avgline]
        if(curClose!='无') and (AvgPrice!='无'):
            Gap = curClose - AvgPrice
            if(Gap > 0):
                Trd_Data.loc[irows,'位置关系'] = '上'
            elif(Gap < 0):
                Trd_Data.loc[irows,'位置关系'] = '下'
        irows = irows + 1
    Trd_Data = Data_AvgL_Dir(Trd_Data,AvgLine)
    writer = ExcelWriter(FilePath2)
    Trd_Data.to_excel(writer,'DataAvgLine')
    writer.save()
    return Trd_Data
#根据位置首张，确定买卖操作，单均线函数2
def SigAvgL_Buy_Sell(stockcode='000001',AnaCycle ='D',FilePath = 'FilePath',AvgLine = 10):
    FilePath = FilePath + '\\'+ stockcode + AnaCycle + str(AvgLine)+ '.xls'
    sheetname ='DataAvgLine'
    AvgL_Data = Get_TrdData_FromExcel(FilePath,sheetname)
    AvgL_Data['操作'] = '无'
    totalrows = len(AvgL_Data)
    irows = 0
    preBS = '无'
    preWZ = AvgL_Data.loc[irows,'位置关系']
    irows = irows + 1
    while(irows < totalrows):
        curWZ = AvgL_Data.loc[irows,'位置关系']
        if(curWZ == preWZ):
            if(preBS == '买入'):
                AvgL_Data.loc[irows,'操作'] ='持股'
            elif(preBS =='卖出'):
                AvgL_Data.loc[irows,'操作'] ='持币'
            irows = irows + 1
        else:
            if(curWZ == '上') and (preWZ !='无'):
                curBS = '买入'
                AvgL_Data.loc[irows,'操作'] = curBS
                preWZ = '上'
                preBS = curBS
            elif(curWZ == '下') and (preWZ !='无'):
                curBS = '卖出'
                AvgL_Data.loc[irows,'操作'] = curBS
                preWZ = '下'
                preBS = curBS
            else:
                preWZ = curWZ
            irows = irows + 1
    sheetname = 'DataAvgLine'
    Write_DF_T0_Excel(FilePath,AvgL_Data,sheetname)
    return AvgL_Data

#单均线结合PE策略：
#根据位置首张，确定买卖操作，单均线函数2
def SigAvgL_PE_Buy_Sell(stockcode='000001',AnaCycle ='D',FilePath = 'FilePath',AvgLine = 10):
    FilePath = FilePath + '\\'+ stockcode + AnaCycle + str(AvgLine)+ '.xls'
    sheetname ='DataAvgLine'
    AvgL_Data = Get_TrdData_FromExcel(FilePath,sheetname)
    AvgL_Data['操作'] = '无'
    totalrows = len(AvgL_Data)
    irows = 0
    preBS = '无'
    preWZ = AvgL_Data.loc[irows,'位置关系']
    irows = irows + 1
    while(irows < totalrows):
        curWZ = AvgL_Data.loc[irows,'位置关系']
        curPE = AvgL_Data.loc[irows,'PE']
        if(curWZ == preWZ):
            if(preBS == '买入'):
                AvgL_Data.loc[irows,'操作'] ='持股'
            elif(preBS =='卖出'):
                AvgL_Data.loc[irows,'操作'] ='持币'
            irows = irows + 1
        else:
            if(curWZ == '上') and (preWZ !='无') and(curPE <50):
                curBS = '买入'
                AvgL_Data.loc[irows,'操作'] = curBS
                preWZ = '上'
                preBS = curBS
            elif(curWZ == '下') and (preWZ !='无') and(curPE >9):
                curBS = '卖出'
                AvgL_Data.loc[irows,'操作'] = curBS
                preWZ = '下'
                preBS = curBS
            else:
                AvgL_Data.loc[irows,'操作'] = AvgL_Data.loc[irows-1,'操作']
                preWZ = curWZ
            irows = irows + 1
    sheetname = 'DataAvgLine'
    Write_DF_T0_Excel(FilePath,AvgL_Data,sheetname)

#根据位置首张，确定买卖操作，单均线函数3,当上穿向下均线或下穿向上均线时，不操作
def SigAvgL_Dir_Buy_Sell(stockcode='000001',AnaCycle ='D',FilePath = 'FilePath',AvgLine = 10):
    FilePath = FilePath + '\\'+ stockcode + AnaCycle + str(AvgLine)+ '.xls'
    sheetname ='DataAvgLine'
    AvgL_Data = Get_TrdData_FromExcel(FilePath,sheetname)
    AvgL_Data['操作'] = '无'
    totalrows = len(AvgL_Data)
    irows = 0
    preBS = '无'
    preWZ = AvgL_Data.loc[irows,'位置关系']
    irows = irows + 1
    while(irows < totalrows):
        curWZ = AvgL_Data.loc[irows,'位置关系']
        curAvgDir = AvgL_Data.loc[irows,'AvgLDir']
        if(curWZ == preWZ):
            if(preBS == '买入'):
                AvgL_Data.loc[irows,'操作'] ='持股'
            elif(preBS =='卖出'):
                AvgL_Data.loc[irows,'操作'] ='持币'
            irows = irows + 1
        else: #上下关系发生变化
            if(curWZ == '上') and (preWZ !='无') and(curAvgDir !='上'):
                if(preBS != '买入'):
                    curBS = '买入'
                    AvgL_Data.loc[irows,'操作'] = curBS
                    preWZ = '上'
                    preBS = curBS
                else:
                    AvgL_Data.loc[irows,'操作'] = '持股'
                    preWZ = '上'
            elif(curWZ == '下') and (preWZ !='无') and(curAvgDir !='下'):
                if(preBS!='卖出'):
                    curBS = '卖出'
                    AvgL_Data.loc[irows,'操作'] = curBS
                    preWZ = '下'
                    preBS = curBS
                else:
                    AvgL_Data.loc[irows,'操作'] = '持币'
                    preWZ = '下'
            else:
                if(preBS =='买入'):
                    AvgL_Data.loc[irows,'操作'] = '持股'
                else:
                    AvgL_Data.loc[irows,'操作'] = '持币'
                preWZ = curWZ
            irows = irows + 1
    sheetname = 'DataAvgLine'
    Write_DF_T0_Excel(FilePath,AvgL_Data,sheetname)

#根据当前价格与中枢的关系结合单均线确定是否买入卖出，其中，在中枢内时，不进行买卖操作
def SigAvgL_ZS_Buy_Sell(stockcode='000001',AnaCycle ='D',FilePath = 'FilePath',AvgLine = 10):
    FilePath = FilePath + '\\'+ stockcode + AnaCycle + str(AvgLine)+ '.xls'
    sheetname ='DataAvgLine'
    AvgL_Data = Get_TrdData_FromExcel(FilePath,sheetname)
    AvgL_Data['操作'] = '无'
    totalrows = len(AvgL_Data)
    irows = 0
    preBS = '无'
    preWZ = AvgL_Data.loc[irows,'位置关系']
    irows = irows + 1
    while(irows < totalrows):
        curWZ = AvgL_Data.loc[irows,'位置关系']
        curZSWZ = AvgL_Data.loc[irows,'中枢关系']
        if(curWZ == preWZ):
            if(preBS == '买入'):
                AvgL_Data.loc[irows,'操作'] ='持股'
            elif(preBS =='卖出'):
                AvgL_Data.loc[irows,'操作'] ='持币'
            irows = irows + 1
        else: #上下关系发生变化
            if(curWZ == '上') and (preWZ !='无') and(curZSWZ!='无'): #(curZSWZ =='上')
                if(preBS != '买入'):
                    curBS = '买入'
                    AvgL_Data.loc[irows,'操作'] = curBS
                    preWZ = '上'
                    preBS = curBS
                else:
                    AvgL_Data.loc[irows,'操作'] = '持股'
                    preWZ = '上'
            elif(curWZ == '下') and (preWZ !='无') and (curZSWZ!='无')and ((curZSWZ=='上')or (curZSWZ=='外上')): #and ((curZSWZ !='内')): #or(curZSWZ=='内')or(curZSWZ=='下')
                if(preBS!='卖出'):
                    curBS = '卖出'
                    AvgL_Data.loc[irows,'操作'] = curBS
                    preWZ = '下'
                    preBS = curBS
                else:
                    AvgL_Data.loc[irows,'操作'] = '持币'
                    preWZ = '下'
            else:
                if(preBS =='买入'):
                    AvgL_Data.loc[irows,'操作'] = '持股'
                else:
                    AvgL_Data.loc[irows,'操作'] = '持币'
                preWZ = curWZ
            irows = irows + 1
    sheetname = 'DataAvgLine'
    Write_DF_T0_Excel(FilePath,AvgL_Data,sheetname)

#突破特定均线即买入，跌破即卖出的策略，单均线多头函数
def AvgL_Long(stockcode='000001',AnaCycle ='D',FilePath = 'FilePath',AvgLine = 5):
    feerate = 0.0016
    FileName = stockcode + AnaCycle+str(AvgLine)
    FilePath2 = FilePath + '\\' + FileName +'AvgLLong.xls'
    FilePath = FilePath + '\\' + FileName +'.xls'
    sheetname = 'DataAvgLine'
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
                if(curOP =='持股'):
                    curValue =  MACD_BS.loc[irows,'close']
                    WinLossPer = curValue/pricecost -1
                    MACD_BS.loc[irows,'盈亏比例'] = WinLossPer
                    irows = irows + 1
                elif(curOP =='卖出'):
                    curValue =  MACD_BS.loc[irows,'close']
                    WinLossPer = curValue/pricecost -1 -feerate
                    MACD_BS.loc[irows,'盈亏比例'] = WinLossPer
                    irows = irows + 1
                else:
                    break
    Write_DF_T0_Excel(FilePath2,MACD_BS,sheetname)

#盈亏比例为当天盈亏

#突破特定均线即买入，跌破即卖出的策略，单均线多头函数,计算每日净值
def AvgL_curLong(stockcode='000001',AnaCycle ='D',FilePath = 'FilePath',AvgLine = 5):
    feerate = 0.0016
    FileName = stockcode + AnaCycle+str(AvgLine)
    FilePath2 = FilePath + '\\' + FileName +'AvgLLong.xls'
    FilePath = FilePath + '\\' + FileName +'.xls'
    sheetname = 'DataAvgLine'
    MACD_BS = Get_TrdData_FromExcel(FilePath,sheetname)
    MACD_BS['当日盈亏比例'] = 0
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
                if(curOP =='持股'):
                    yesValue = MACD_BS.loc[irows-1,'close']
                    curValue =  MACD_BS.loc[irows,'close']
                    WinLossPer = curValue/yesValue -1
                    MACD_BS.loc[irows,'当日盈亏比例'] = WinLossPer
                    irows = irows + 1
                elif(curOP =='卖出'):
                    yesValue = MACD_BS.loc[irows-1,'close']
                    curValue =  MACD_BS.loc[irows,'close']
                    WinLossPer = curValue/yesValue -1 -feerate
                    MACD_BS.loc[irows,'当日盈亏比例'] = WinLossPer
                    irows = irows + 1
                else:
                    break
    irows = 0
    NetValue = 1
    while(irows < totalrows):
        curDayWinLoss = MACD_BS.loc[irows,'当日盈亏比例']
        NetValue = NetValue * (1+curDayWinLoss)
        MACD_BS.loc[irows,'当日净值(多头)'] = NetValue
        irows = irows + 1
    Write_DF_T0_Excel(FilePath2,MACD_BS,sheetname)

#跌破即开空，突破即平仓的策略,单均线空头策略,计算当下作空净值
def AvgL_curShort(stockcode='000001',AnaCycle ='D',FilePath = 'FilePath',AvgLine = 5):
    FileName = stockcode + AnaCycle+str(AvgLine)
    FilePath2 = FilePath + '\\' + FileName +'AvgLShort.xls'
    FilePath = FilePath + '\\' + FileName +'.xls'
    sheetname = 'DataAvgLine'
    MACD_BS = Get_TrdData_FromExcel(FilePath,sheetname)
    MACD_BS['当日盈亏比例'] = 0
    totalrows = len(MACD_BS)
    irows = 0
    #找到第一个卖出操作
    while(irows < totalrows):
        curOP = MACD_BS.loc[irows,'操作']
        if(curOP != '卖出'):
            irows = irows + 1
        else:
            irows = irows + 1
            while(irows < totalrows):
                curOP = MACD_BS.loc[irows,'操作']
                if(curOP =='持币') :
                    preValue = MACD_BS.loc[irows-1,'close']
                    curValue =  MACD_BS.loc[irows,'close']
                    WinLossPer = (preValue-curValue)/preValue
                    MACD_BS.loc[irows,'当日盈亏比例'] = WinLossPer #*2
                    irows = irows + 1
                elif(curOP =='买入'):
                    feerate = 0.00006
                    preValue = MACD_BS.loc[irows-1,'close']
                    curValue =  MACD_BS.loc[irows,'close']
                    WinLossPer = (preValue-curValue)/preValue
                    MACD_BS.loc[irows,'当日盈亏比例'] = (WinLossPer - 0.00003) *2
                    irows = irows + 1
                else:
                    break
    irows = 0
    NetValue = 1
    while(irows < totalrows):
        curDayWinLoss = MACD_BS.loc[irows,'当日盈亏比例']
        NetValue = NetValue * (1+curDayWinLoss)
        MACD_BS.loc[irows,'当日净值(空头)'] = NetValue
        irows = irows + 1
    MACD_BS = DateMerge(MACD_BS)
    Write_DF_T0_Excel(FilePath2,MACD_BS,sheetname)

#跌破即开空，突破即平仓的策略,单均线空头策略
def AvgL_Short(stockcode='000001',AnaCycle ='D',FilePath = 'FilePath',AvgLine = 5):
    FileName = stockcode + AnaCycle+str(AvgLine)
    FilePath2 = FilePath + '\\' + FileName +'AvgLShort.xls'
    FilePath = FilePath + '\\' + FileName +'.xls'
    sheetname = 'DataAvgLine'
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

#插入列标示均线当下方向，用三个连续值的升降确定
def Data_AvgL_Dir(Trd_Data = 'Trd_Data',AvgLine = 10):
    Trd_Data['AvgLDir'] = '无'
    totalrows = len(Trd_Data)
    irows = 0
    totalValue = 0
    while(irows < totalrows):
        curAvg = Trd_Data.loc[irows,'Avg'+str(AvgLine)]
        if(irows <AvgLine + 1):
            Trd_Data.loc[irows,'AvgLDir'] = '无'
        else:
            AvgP1 = Trd_Data.loc[irows-2,'Avg'+str(AvgLine)]
            AvgP2 = Trd_Data.loc[irows-1,'Avg'+str(AvgLine)]
            AvgP3 = Trd_Data.loc[irows,'Avg'+str(AvgLine)]
            if(AvgP1 > AvgP2) and (AvgP2 > AvgP3):
                AvgDir = '下'
            elif(AvgP1 < AvgP2) and (AvgP2 < AvgP3):
                AvgDir = '上'
            else:
                AvgDir = '无'
            Trd_Data.loc[irows,'AvgLDir'] = AvgDir
        irows = irows + 1

    return Trd_Data


#----------------------------------------------------------------------------------------------------------------------------------
#计算两条均线之间的上下关系
def DouMVAg_WZ(stockcode='000001',AnaCycle ='D',FilePath = 'FilePath',AvgLShort = 5,AvgLLong = 10):
    Avgl = str(AvgLShort) +'-'+ str(AvgLLong)
    FilePath2 = FilePath + '\\'+ stockcode + AnaCycle +Avgl +'.xls'
    FilePath = FilePath + '\\'+ stockcode + AnaCycle + '.xls'
    sheetname ='OriData'
    Trd_Data = Get_TrdData_FromExcel(FilePath,sheetname)
    Trd_Data = Data_Avg_Line(Trd_Data,AvgLShort)
    Trd_Data = Data_Avg_Line(Trd_Data,AvgLLong)
    Trd_Data['位置关系'] = '无'
    irows = 0
    totalrows = len(Trd_Data)
    Avgline1 = 'Avg'+str(AvgLShort)
    Avgline2 = 'Avg'+str(AvgLLong)
    while(irows < totalrows):
        AvgPrice1 = Trd_Data.loc[irows,Avgline1]
        AvgPrice2 = Trd_Data.loc[irows,Avgline2]
        if(AvgPrice1!='无') and (AvgPrice2!='无'):
            Gap = AvgPrice1 - AvgPrice2
            if(Gap > 0):
                Trd_Data.loc[irows,'位置关系'] = '上'
            elif(Gap < 0):
                Trd_Data.loc[irows,'位置关系'] = '下'
        irows = irows + 1
    writer = ExcelWriter(FilePath2)
    Trd_Data.to_excel(writer,'DataAvgLine')
    writer.save()

#双均线策略，短上穿长买入，长下穿短卖出
def DouAvgL_Buy_Sell(stockcode='000001',AnaCycle ='D',FilePath = 'FilePath',AvgLShort = 5,AvgLLong = 10):
    FilePath = FilePath + '\\'+ stockcode + AnaCycle + str(AvgLShort)+'-'+str(AvgLLong)+ '.xls'
    sheetname ='DataAvgLine'
    AvgL_Data = Get_TrdData_FromExcel(FilePath,sheetname)
    AvgL_Data['操作'] = '无'
    totalrows = len(AvgL_Data)
    irows = 0
    preBS = '无'
    preWZ = AvgL_Data.loc[irows,'位置关系']
    irows = irows + 1
    while(irows < totalrows):
        curWZ = AvgL_Data.loc[irows,'位置关系']
        if(curWZ == preWZ):
            if(preBS == '买入'):
                AvgL_Data.loc[irows,'操作'] ='持股'
            elif(preBS =='卖出'):
                AvgL_Data.loc[irows,'操作'] ='持币'
            irows = irows + 1
        else:
            if(curWZ == '上') and (preWZ !='无'):
                curBS = '买入'
                AvgL_Data.loc[irows,'操作'] = curBS
                preWZ = '上'
                preBS = curBS
            elif(curWZ == '下') and (preWZ !='无'):
                curBS = '卖出'
                AvgL_Data.loc[irows,'操作'] = curBS
                preWZ = '下'
                preBS = curBS
            else:
                preWZ = curWZ
            irows = irows + 1
    sheetname = 'DataAvgLine'
    Write_DF_T0_Excel(FilePath,AvgL_Data,sheetname)

#双均线策略，短上穿长买入，长下穿短卖出,中枢内不做
def DouAvgL_ZS_Buy_Sell(stockcode='000001',AnaCycle ='D',FilePath = 'FilePath',AvgLShort = 5,AvgLLong = 10):
    FilePath = FilePath + '\\'+ stockcode + AnaCycle + str(AvgLShort)+'-'+str(AvgLLong)+ '.xls'
    sheetname ='DataAvgLine'
    AvgL_Data = Get_TrdData_FromExcel(FilePath,sheetname)
    AvgL_Data['操作'] = '无'
    totalrows = len(AvgL_Data)
    irows = 0
    preBS = '无'
    preWZ = AvgL_Data.loc[irows,'位置关系']
    irows = irows + 1
    while(irows < totalrows):
        curWZ = AvgL_Data.loc[irows,'位置关系']
        curZSWZ = AvgL_Data.loc[irows,'中枢关系']
        if(curWZ == preWZ):
            if(preBS == '买入'):
                AvgL_Data.loc[irows,'操作'] ='持股'
            elif(preBS =='卖出'):
                AvgL_Data.loc[irows,'操作'] ='持币'
            irows = irows + 1
        else:
            if(curWZ == '上') and (preWZ !='无') and(curZSWZ!='无')and((curZSWZ=='下') or(curZSWZ=='上') or(curZSWZ=='外上')): #(curZSWZ =='上')
                if(preBS != '买入'):
                    curBS = '买入'
                    AvgL_Data.loc[irows,'操作'] = curBS
                    preWZ = '上'
                    preBS = curBS
                else:
                    AvgL_Data.loc[irows,'操作'] = '持股'
                    preWZ = '上'
            elif(curWZ == '下') and (preWZ !='无') and (curZSWZ!='无')and ((curZSWZ=='上')): #and ((curZSWZ !='内')): #or(curZSWZ=='内')or(curZSWZ=='下')
                if(preBS!='卖出'):
                    curBS = '卖出'
                    AvgL_Data.loc[irows,'操作'] = curBS
                    preWZ = '下'
                    preBS = curBS
                else:
                    AvgL_Data.loc[irows,'操作'] = '持币'
                    preWZ = '下'
            else:
                if(preBS =='买入'):
                    AvgL_Data.loc[irows,'操作'] = '持股'
                else:
                    AvgL_Data.loc[irows,'操作'] = '持币'
                preWZ = curWZ
            irows = irows + 1
    sheetname = 'DataAvgLine'
    Write_DF_T0_Excel(FilePath,AvgL_Data,sheetname)

#双均线盈亏比例计算,空头的持仓盈亏
#跌破即开空，突破即平仓的策略
def DouAvgL_Short(stockcode='000001',AnaCycle ='D',FilePath = 'FilePath',AvgLShort = 5,AvgLLong = 10):
    FileName = stockcode + AnaCycle+str(AvgLShort)+'-'+str(AvgLLong)+'.xls'
    FilePath2 = FilePath + '\\' + stockcode + AnaCycle+str(AvgLShort)+'-'+str(AvgLLong) +'AvgLShort.xls'
    FilePath = FilePath + '\\' + FileName
    sheetname = 'DataAvgLine'
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
#双均线盈亏比例计算,多头的持仓盈亏
def DouAvgL_Long(stockcode='000001',AnaCycle ='D',FilePath = 'FilePath',AvgLShort = 5,AvgLLong = 10):
    FileName = stockcode + AnaCycle+str(AvgLShort)+'-'+str(AvgLLong)+'.xls'
    FilePath2 = FilePath + '\\' + stockcode + AnaCycle+str(AvgLShort)+'-'+str(AvgLLong) +'AvgLLong.xls'
    FilePath = FilePath + '\\' + FileName
    sheetname = 'DataAvgLine'
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


#----------------------------------------------------------------------------------------------------------------------

#策略，MACD黄白线,用简单平均值
def MACD_RWL(Trd_Data='Trd_Data',FilePath='FilePath'):
    Trd_Data = Data_Avg_Line(Trd_Data,12)
    Trd_Data = Data_Avg_Line(Trd_Data,26)
    return Trd_Data

#计算白线DIF
def Data_MACD_DIF(Trd_Data = 'Trd_Data'):
    Trd_Data['DIF'] = '无'
    totalrows = len(Trd_Data)
    irows = 0
    while(irows < totalrows):
        Avg12 = Trd_Data.loc[irows,'Avg12']
        Avg26 = Trd_Data.loc[irows,'Avg26']
        if(Avg12 !='无') and (Avg26 !='无'):
            Trd_Data.loc[irows,'DIF'] = Avg12 - Avg26
        irows = irows + 1
    return Trd_Data

#计算黄线DEA
def Data_MACD_DEA(Trd_Data = 'Trd_Data'):
    Trd_Data['DEA'] = '无'
    totalrows = len(Trd_Data)
    irows = 0
    totalValue = 0
    n = 9
    while(irows < totalrows):
        DIF = Trd_Data.loc[irows,'DIF']
        if (DIF == '无'):
            irows = irows + 1
        else:
            nrows = irows
            break
    while(irows < totalrows):
        if(irows < nrows + n-1):
            DIF = Trd_Data.loc[irows,'DIF']
            totalValue = totalValue + DIF
            irows =irows + 1
            nrow = irows
        elif (irows == nrows + n-1):
            DIF = Trd_Data.loc[irows,'DIF']
            totalValue = totalValue + DIF
            avgValue = totalValue/n
            Trd_Data.loc[irows,'DEA'] = avgValue
            irows = irows + 1
        else:
            DIF = Trd_Data.loc[irows,'DIF']
            totalValue = totalValue + DIF - Trd_Data.loc[irows-n,'DIF']
            avgValue = totalValue/n
            Trd_Data.loc[irows,'DEA'] = avgValue
            irows = irows + 1
    return Trd_Data



#计算给定交易标的的DIF，DEA，并将其保存在指定文件中,算法用移动平均，而非向后加权
def MACD_DIF_DEA_MV(stockcode='000001',AnaCycle ='D',FilePath = 'FilePath'):
    FileName = stockcode + AnaCycle
    FilePath1 = FilePath + '\\' + FileName +'.xls'
    FilePath2 =  FilePath + '\\' + FileName +'MACD.xls'
    SheetName = 'OriData'
    Ori_Data = Get_TrdData_FromExcel(FilePath1,SheetName)
    Trd_Data = ReIndex(Ori_Data)
    Trd_Data = MACD_RWL(Trd_Data,FilePath)
    Trd_Data = Data_MACD_DIF(Trd_Data)
    Trd_Data = Data_MACD_DEA(Trd_Data)
    totalrows = len(Trd_Data)
    irows = 0
    Trd_Data['位置关系'] = '无'
    while(irows < totalrows):
        DIF = Trd_Data.loc[irows,'DIF']
        DEA = Trd_Data.loc[irows,'DEA']
        if(DIF!='无') and (DEA!='无'):
            Gap = DIF -DEA
            if(Gap > 0):
                Trd_Data.loc[irows,'位置关系'] = '上'
            elif(Gap < 0):
                Trd_Data.loc[irows,'位置关系'] = '下'
        irows = irows + 1
    writer = ExcelWriter(FilePath2)
    Trd_Data.to_excel(writer,'MACDData')
    writer.save()
    return Trd_Data

#计算给定交易标的的DIF，DEA，并将其保存在指定文件中,算法用加权移动平均（EMA）
def MACD_DIF_DEA_EMV(stockcode='000001',AnaCycle ='D',FilePath = 'FilePath'):
    FileName = stockcode + AnaCycle
    FilePath1 = FilePath + '\\' + FileName +'.xls'
    FilePath2 =  FilePath + '\\' + FileName +'MACD.xls'
    SheetName = 'OriData'
    Ori_Data = Get_TrdData_FromExcel(FilePath1,SheetName)
    Trd_Data = Data_MACD_BAR(Ori_Data)
    Trd_Data['位置关系'] = '无'
    totalrows = len(Trd_Data)
    irows = 0
    while(irows < totalrows):
        DIF = Trd_Data.loc[irows,'DIF']
        DEA = Trd_Data.loc[irows,'DEA']
        if(DIF!='无') and (DEA!='无'):
            Gap = DIF -DEA
            if(Gap > 0):
                Trd_Data.loc[irows,'位置关系'] = '上'
            elif(Gap < 0):
                Trd_Data.loc[irows,'位置关系'] = '下'
        irows = irows + 1
    writer = ExcelWriter(FilePath2)
    Trd_Data.to_excel(writer,'')
    writer.save()
    return Trd_Data

#策略，MACD黄白线白线空黄线时买入，黄线穿白线时卖出,这时黄白线计算采用Moving Average，而不是EMA
def MACD_Buy_Sell(stockcode='000001',AnaCycle ='D',FilePath = 'FilePath'):
    FileName = stockcode + AnaCycle
    FilePath = FilePath + '\\' + FileName +'MACD.xls'
    sheetname = 'MACDData'
    MACD_Data = Get_TrdData_FromExcel(FilePath,sheetname)
    MACD_Data['操作'] = '无'
    totalrows = len(MACD_Data)
    irows = 0
    preBS = '无'
    preWZ = MACD_Data.loc[irows,'位置关系']
    irows = irows + 1
    while(irows < totalrows):
        curWZ = MACD_Data.loc[irows,'位置关系']
        if(curWZ == preWZ):
            if(preBS == '买入'):
                MACD_Data.loc[irows,'操作'] ='持股'
            elif(preBS =='卖出'):
                MACD_Data.loc[irows,'操作'] ='持币'
            irows = irows + 1
        else:
            if(curWZ == '上') and (preWZ !='无'):
                curBS = '买入'
                MACD_Data.loc[irows,'操作'] = curBS
                preWZ = '上'
                preBS = curBS
            elif(curWZ == '下'):
                curBS = '卖出'
                MACD_Data.loc[irows,'操作'] = curBS
                preWZ = '下'
                preBS = curBS
            irows = irows + 1
    sheetname = 'MACDData'
    Write_DF_T0_Excel(FilePath,MACD_Data,sheetname)

#黄白线上穿,DIF，DEA均为正买入，下穿，DIF,DEA均为负卖出
def MACD_Buy_Sell_Plus(stockcode='000001',AnaCycle ='D',FilePath = 'FilePath'):
    FileName = stockcode + AnaCycle
    FilePath = FilePath + '\\' + FileName +'MACD.xls'
    sheetname = 'MACDData'
    MACD_Data = Get_TrdData_FromExcel(FilePath,sheetname)
    MACD_Data['操作'] = '无'
    totalrows = len(MACD_Data)
    irows = 0
    preBS = '无'
    preWZ = MACD_Data.loc[irows,'位置关系']
    irows = irows + 1
    while(irows < totalrows):
        preWZ = MACD_Data.loc[irows-1,'位置关系']
        curWZ = MACD_Data.loc[irows,'位置关系']
        if(curWZ == preWZ):
            if(preBS == '买入'):
                MACD_Data.loc[irows,'操作'] ='持股'
            elif(preBS =='卖出'):
                MACD_Data.loc[irows,'操作'] ='持币'
            irows = irows + 1
        else:
            if(curWZ == '上') and (preWZ =='下') :
                DIF = MACD_Data.loc[irows,'DIF']
                DEA = MACD_Data.loc[irows,'DEA']
                if(DIF > 0) and (DEA > 0):
                    curBS = '买入'
                    MACD_Data.loc[irows,'操作'] = curBS
                    preBS = curBS
                else:
                    curBS =  MACD_Data.loc[irows-1,'操作']
                    MACD_Data.loc[irows,'操作'] = curBS

            elif(curWZ == '下') and(preWZ=='上'):
                DIF = MACD_Data.loc[irows,'DIF']
                DEA = MACD_Data.loc[irows,'DEA']
                if(DIF <0) and (DEA < 0):
                    curBS = '卖出'
                    MACD_Data.loc[irows,'操作'] = curBS
                    preBS = curBS
                else:
                    curBS =  MACD_Data.loc[irows-1,'操作']
                    MACD_Data.loc[irows,'操作'] = curBS
            irows = irows + 1
    irows = 0
    #去掉连续的买和卖
    while(irows < totalrows):
        curBS =  MACD_Data.loc[irows,'操作']
        if(curBS!='买入') and (curBS !='卖出'):
            irows = irows + 1
        else:
            irows =irows + 1
            preBS = curBS
            break
    while (irows < totalrows):
        curBS =  MACD_Data.loc[irows,'操作']
        if(curBS!='买入') and (curBS !='卖出'):
            irows = irows + 1
        elif(curBS == preBS):
            MACD_Data.loc[irows,'操作'] = MACD_Data.loc[irows-1,'操作']
            irows = irows + 1
        else:
            preBS = curBS
            irows = irows + 1
    sheetname = 'MACDData'
    Write_DF_T0_Excel(FilePath,MACD_Data,sheetname)



#在数据中插入列，列的内容为指定日期的均线：
def Data_Avg_Line(Trd_Data = 'Trd_Data', n = 15):
    AvgLine = 'Avg' + str(n)
    Trd_Data[AvgLine] = '无'
    totalrows = len(Trd_Data)
    irows = 0
    totalValue = 0
    while(irows < totalrows):
        if(irows <n-1):
            close = Trd_Data.loc[irows,'close']
            totalValue = totalValue + close
            irows =irows + 1
        elif (irows == n-1):
            close = Trd_Data.loc[irows,'close']
            totalValue = totalValue + close
            avgValue = totalValue/n
            Trd_Data.loc[irows,AvgLine] = avgValue
            irows = irows + 1
        else:
            close = Trd_Data.loc[irows,'close']
            totalValue = totalValue + close - Trd_Data.loc[irows-n,'close']
            avgValue = totalValue/n
            Trd_Data.loc[irows,AvgLine] = avgValue
            irows = irows + 1
    return Trd_Data

#数据合并，将日线级别以下交易的净值按最后一笔并入新的数据表，并返回,主要用于小于日线级别的操作时净值统计
def DateMerge(Trd_Data = 'TrdData'):
    df = DataFrame([],columns=Trd_Data.columns)
    totalrows = len(Trd_Data)
    irows = 0
    preDate = str(Trd_Data.loc[irows,'date'])
    preDate = preDate[0:10]
    irows = irows + 1
    while(irows < totalrows):
        curDate = str(Trd_Data.loc[irows,'date'])
        curDate = curDate[0:10]
        if(curDate == preDate):
            irows = irows + 1
        else:
            s = Trd_Data.iloc[irows-1]
            df = df.append(s)
            irows = irows + 1
            preDate = curDate
    return df

#用5分钟2:55的收盘价代替日线收盘价，存入数据库表中,由两个程序组成
#将5分钟的数据按2：55价格，合并为每日一笔，返回数据表中，仅close有意义
def DateFiveSimu(Trd_Data = 'TrdData'):
    df = DataFrame([],columns=Trd_Data.columns)
    totalrows = len(Trd_Data)
    irows = 0
    preDate = str(Trd_Data.loc[irows,'date'])
    preDate = preDate[0:10]
    irows = irows + 1
    while(irows < totalrows):
        curDate = str(Trd_Data.loc[irows,'date'])
        curDate = curDate[0:10]
        if(curDate == preDate):
            irows = irows + 1
        else:
            s = Trd_Data.iloc[irows-2]
            df = df.append(s)
            irows = irows + 1
            preDate = curDate
    df = ReIndex(df)
    return df

#用五分钟的2:55价格代替日线收盘价，并将数据存储到另一张数据表中,默认日线数据比五分钟数据的存续日期久，这一逻辑未必正确，未来仍要修改
def DataSimu(Trd_Day = 'Trd_Day',Trd_FiveM = 'Trd_FiveM'):
    Trd_FiveM = DateFiveSimu(Trd_FiveM)
    FiveMStart =str(Trd_FiveM.loc[0,'date'])
    FiveMStart = FiveMStart[0:10]
    DayIndex = 0
    Day_Start = str(Trd_Day.loc[0,'date'])
    Day_Start = Day_Start[0:10]
    while(Day_Start != FiveMStart):
        DayIndex = DayIndex + 1
        Day_Start = str(Trd_Day.loc[0,'date'])
        Day_Start = Day_Start[0:10]
    totalFives = len(Trd_FiveM)
    totalDays = len(Trd_Day)
    FiveIndex = 0
    while (FiveIndex < totalFives) and ((FiveIndex+ DayIndex) <totalDays):
        Trd_Day.loc[FiveIndex+ DayIndex,'close'] = Trd_FiveM.loc[FiveIndex,'close']
        FiveIndex = FiveIndex + 1
    FilePath = 'D:\Chan Data\MNiCompare\hs300D2.xls'
    Write_DF_T0_Excel(FilePath,Trd_Day,'OriData')

#2:55和3:00做收盘价的效果比较：
def DayFive_Compare():
    stockcode='hs300'
    AnaCycle = 'D'
    FilePath = 'D:\Chan Data\MNiCompare'
    AvgLine = 20
    Trd_Data1 = MVAg_WZ(stockcode,AnaCycle,FilePath,AvgLine)
    AnaCycle2 = 'D2'
    Trd_Data2 = MVAg_WZ(stockcode,AnaCycle2,FilePath,AvgLine)
    totalrows = len(Trd_Data1)
    irows = 0
    Trd_Data1['均线2'] = '无'
    Trd_Data1['位置关系2'] = '无'
    Trd_Data1['新收盘'] = '无'
    difCounter = 0
    while(irows < totalrows):
        Trd_Data1.loc[irows,'均线2'] = Trd_Data2.loc[irows,'Avg20']
        Trd_Data1.loc[irows,'位置关系2'] = Trd_Data2.loc[irows,'位置关系']
        Trd_Data1.loc[irows,'新收盘'] = Trd_Data2.loc[irows,'close']
        if(Trd_Data1.loc[irows,'位置关系2']!=Trd_Data1.loc[irows,'位置关系']):
            difCouner =difCounter + 1
        irows = irows + 1
    FilePath3 = 'D:\Chan Data\MNiCompare\hs300D3.xls'
    Write_DF_T0_Excel(FilePath3,Trd_Data1,'OriData')


#将指定列表中的股票下载到特定的文件夹，并计算股票的均线值，以及位置关系，然后将结果存储到该文件夹中
def StockList_AvgData_Down(Stock_Code_list = 'Stock_Code_list',FilePath = 'FilePath',AnaCycle='D',
                    startDate='startDate',endDate='endDate',AvgLine = 20):
    irows = 0
    totalrows = len(Stock_Code_list)
    AboveCounter = 0
    BelowCounter = 0
    df = DataFrame([],columns=['stockcode','名称'])
    while(irows < totalrows):
        stockcode = Stock_Code_list.loc[irows,'stockcode']
        stockcode = codeType(stockcode)
        stockName = Stock_Code_list.loc[irows,'名称']
        stockcode = codeType(stockcode)
        Trd_Data = Get_TrData_FromTs(StockCode = stockcode,AnaCycle = AnaCycle,startDate = startDate,endDate =endDate)
        FilePath2 = FilePath +'\\'+ stockcode+AnaCycle+ '.xls'
        #返回带均线的数据
        Trd_Data = Data_Avg_Line(Trd_Data,AvgLine)
        Trd_Data['位置关系'] = '无'
        irowsTrd = 0
        totalrowsTrd = len(Trd_Data)
        print(stockcode,totalrowsTrd)
        Avgline = 'Avg'+str(AvgLine)
        while(irowsTrd < totalrowsTrd):
            curClose = Trd_Data.loc[irowsTrd,'close']
            AvgPrice = Trd_Data.loc[irowsTrd,Avgline]
            if(curClose!='无') and (AvgPrice!='无'):
                Gap = curClose - AvgPrice
                if(Gap > 0):
                    Trd_Data.loc[irowsTrd,'位置关系'] = '上'
                elif(Gap < 0):
                    Trd_Data.loc[irowsTrd,'位置关系'] = '下'
            irowsTrd = irowsTrd + 1
        writer = ExcelWriter(FilePath2)
        Trd_Data.to_excel(writer,'DataAvgLine')
        writer.save()
        LastWZ = Trd_Data.loc[totalrowsTrd-1,'位置关系']
        if(LastWZ =='上'):
            AboveCounter = AboveCounter + 1
        elif(LastWZ =='下'):
            BelowCounter = BelowCounter + 1
            s = Stock_Code_list.iloc[irows]
            df = df.append(s)
        irows = irows + 1
    return AboveCounter,BelowCounter,df

#将中枢数据插入到特定目录
def AddPivotData(stockcode = '',AnaCycle = 'D',FilePath = ''):
    FilePath2 = FilePath + '\\'+stockcode + AnaCycle + '.xls'
    Pivot_Data = AddPivotSheet(FilePath,stockcode,AnaCycle)
    return Pivot_Data

#根据输入的日期找到离当下日期最近的中枢
def Latest_ZS_Before(Pivot_Data = 'Pivot_Data',curdate = 'curdate'):
    if(curdate=='2010-08-12'):
        print(curdate)
    totalrows = len(Pivot_Data)
    irowsCounter = 0
    ZSData = Series(['无','无','无','无'],index=['ZD','ZG','DD','GG'])
    while(irowsCounter < totalrows):
        endDate = Pivot_Data.loc[irowsCounter,'endDate']
        if(endDate > curdate):
            break
        else:
            irowsCounter = irowsCounter + 1
    irowsCounter = irowsCounter -2
    while(irowsCounter >= 0):
        ZD = Pivot_Data.loc[irowsCounter,'ZD']
        if(ZD!='无'):
            ZG = Pivot_Data.loc[irowsCounter,'ZG']
            DD = Pivot_Data.loc[irowsCounter,'DD']
            GG = Pivot_Data.loc[irowsCounter,'GG']
            ZSData['ZD'] = ZD
            ZSData['ZG'] = ZG
            ZSData['DD'] = DD
            ZSData['GG'] = GG
            break
        else:
            irowsCounter = irowsCounter -1
    return ZSData

#根据中枢数据，确定股票与中枢的关系：
def AddZSWZ(stockcode = '',AnaCycle = 'D',FilePath = ''):
    FilePath2 = FilePath + '\\'+stockcode + AnaCycle + '.xls'
    Trd_Data = Get_TrdData_FromExcel(FilePath2,'OriData')
    sheetName = AnaCycle + 'Bi'
    PivotData = Get_TrdData_FromExcel(FilePath2,sheetName)
    Trd_Data['中枢关系'] = '外'
    totalTrd = len(Trd_Data)
    iDay = 0
    while(iDay < totalTrd):
        curdate = Trd_Data.loc[iDay,'date']
        zsData = Latest_ZS_Before(PivotData,curdate)
        ZD = zsData['ZD']
        ZG = zsData['ZG']
        DD = zsData['DD']
        GG = zsData['GG']
        if(ZD!='无'):
            curClose = Trd_Data.loc[iDay,'close']
            if(curClose>ZD) and(curClose<ZG):
                Trd_Data.loc[iDay,'中枢关系'] = '内'
            elif (curClose>GG):
                Trd_Data.loc[iDay,'中枢关系'] = '上'
            elif(curClose<DD):
                Trd_Data.loc[iDay,'中枢关系'] = '下'
            elif(curClose > ZG):
                Trd_Data.loc[iDay,'中枢关系'] = '外上'
            elif(curClose < ZD):
                Trd_Data.loc[iDay,'中枢关系'] = '外下'
        else:
            Trd_Data.loc[iDay,'中枢关系'] = '无'
        iDay = iDay + 1
    writer = ExcelWriter(FilePath2)
    Trd_Data.to_excel(writer,'OriData')
    sheetName = AnaCycle + 'Bi'
    PivotData.to_excel(writer,sheetName)
    writer.save()








