# -*- coding: utf-8 -*-
from DataProcess import *
from DataInter import *
from DataPlot import *
import datetime
from GenProcess import *
import pandas as pd
from StrProcess import *
# -*- coding: utf-8 -*-
from DataProcess import *
from DataInter import *
from DataPlot import *
import datetime
from GenProcess import *
import pandas as pd
from StrProcess import *

#处理一切与中枢关系相关的操作：
#应用1，根据输入的代码和周期，处理所有历史数据
#数据应用1，根据输入代码，在周线和日线级别做出全数据处理，对于日线或周线最后一个确定分型后的30分钟和5分钟进行处理，从而进行区间套判断
def AllCyclePro(StockCode = 'sh'):
    StockCode = StockCode
    AnaCycle = 'W'
    LV0_Bi_Data,LastBiTrend = Lv1Process(StockCode,AnaCycle)
    AnaCycle = 'D'
    LV1_Bi_Data,LastBiTrend = Lv1Process(StockCode,AnaCycle)
    AnaCycle = '30'
    today = get_Trday_of_day(0)
    LV2_Bi_Data = Lv2Process(StockCode,AnaCycle,startDate = LV1_Bi_Data, endData= today,LastBiTrend =LastBiTrend)
    AnaCycle = '5'
    today = get_Trday_of_day(0)
    LV3_Bi_Data = Lv2Process(StockCode,AnaCycle,startDate = LV1_Bi_Data, endData= today,LastBiTrend =LastBiTrend)

#应用2：数据展示，在30分钟，5分钟显示日线的笔
def BiDemo(dayFrame='dayFrame',thirFrame='thirFrame',fiveFrame='fiveFrame'):
    thirStart,thirEnd = Trd_TimeSpan(thirFrame)
    fiveStart,fiveEnd = Trd_TimeSpan(fiveFrame)
    DayBi = Bi_in_time(dayFrame,thirStart,thirEnd)
    BiPlot(DayBi)
    irows = 0
    totalrows = len(dayFrame)
    while(irows< totalrows):
        startDate = dayFrame.loc[irows,'startDate']
        endDate = dayFrame.loc[irows,'endDate']
        if(startDate < thirStart) or (startDate < fiveStart):
            irows = irows + 1
        elif (endDate >thirEnd) or (endDate>fiveEnd):
            break
        else:
            endDate = endDate + timedelta(1)
            thirBi = Bi_in_time(thirFrame,startDate,endDate)
            BiPlot(thirBi)
            length = len(thirBi)
            if(length <=3):
                fiveBi = Bi_in_time(fiveFrame,startDate,endDate)
                BiPlot(fiveBi)
            irows = irows + 1

#选股策略一
#找到日线3(可选)个交易日为连续下降K线（包含处理后）且30分钟属于盘背段的股票，如果总数小于40支，进一步限定日线盘背的股票
#DBot_SD,DBot_ED,日线顶底分型起止日期；DPB_SD,DPB_ED，日盘背起止日期；
# TMPB_SD,TMPB_ED 30分钟盘背起止点；FM3B_SD,FM3B_ED 5分钟三买判断起止日期
#应用情影大盘出现底分型或在低位横整时
def Sel_Stock_PB3BDFX(n = 0):
    DBot_SD = get_Trday_of_day(n+3)
    DBot_ED = get_Trday_of_day(n)
    DPB_SD = get_Trday_of_day(n+120)
    DPB_ED = get_Trday_of_day(n)
    TMPB_SD = get_Trday_of_day(n+15)
    TMPB_ED = get_Trday_of_day(8*n,'30')
    FM3B_SD = get_Trday_of_day(n+3)
    FM3B_ED = get_Trday_of_day(48*n,'5')
    stock_code_list = Sel_StockPB3BDFX(DBot_SD,DBot_ED,DPB_SD,DPB_ED,TMPB_SD,TMPB_ED,FM3B_SD,FM3B_ED)
    return stock_code_list

def Sel_StockPB3BDFX(DBot_SD,DBot_ED,DPB_SD,DPB_ED,TMPB_SD,TMPB_ED,FM3B_SD,FM3B_ED):
    enddate = DBot_ED
    FilePath = 'D:\Chan Data\Selected Stock\Str1\Date'+enddate+ '.xls'
#    list = get_all_stock()
    list = get_hs300stock()
    print(list)
    stock_code_list = get_stock_end_dkx(stock_code_list = list,begindate =DBot_SD, enddate = DBot_ED,AnaCycle='D')
    Write_to_txt('BotData.txt',stock_code_list)
    stock_code_list =Read_from_txt(fileName = 'BotData.txt')
    stock_code_list = get_stock_panbei(stock_code_list=stock_code_list,AnaCycle='30',begindate=TMPB_SD,enddate=TMPB_ED,Dir='下')
    Write_to_txt('PanBei.txt',stock_code_list)
    stock_code_list = Read_from_txt(fileName = 'PanBei.txt')
    totalrows = len(stock_code_list)
    if(totalrows < 10): #结果小于10支时不再继续执行，返回日线有底分型，30分钟盘背的股票
        Write_STo_Excel(FilePath ,stock_code_list,'StockList')
    else:
        stock_code_list =Read_from_txt(fileName = 'PanBei.txt')
        stock_code_list = get_stock_panbei(stock_code_list=stock_code_list,AnaCycle='D',begindate=DPB_SD,enddate=DPB_ED,Dir='下')
        Write_to_txt('DouPanBei.txt',stock_code_list)
        stock_code_list = Read_from_txt(fileName = 'DouPanBei.txt')
        stock_code_list.append('sh')
        stock_code_list.append('sz')
        Write_STo_Excel(FilePath ,stock_code_list,'StockList')
    return stock_code_list


#选股策略二，日线在4个交易日内出现底分型，且5分钟出现三买，操盘级别为5分钟，操盘周期短
def Sel_Stock_DB3B(n=0):
    DBot_SD = get_Trday_of_day(n+3)
    DBot_ED = get_Trday_of_day(n)
    FM3B_SD = get_Trday_of_day(n+2)
    FM3B_ED = get_Trday_of_day(n)
    stock_code_list = Sel_StockDB3B(DBot_SD,DBot_ED,FM3B_SD,FM3B_ED)
    return stock_code_list

def Sel_StockDB3B(DBot_SD,DBot_ED,FM3B_SD,FM3B_ED):
    enddate = DBot_ED
    FilePath = 'D:\Chan Data\Selected Stock\Str2\Date'+enddate+ '.xls'
    list = get_all_stock()
    stock_code_list = get_stock_end_bot(stock_code_list = list,begindate =DBot_SD, enddate = DBot_ED )
    Write_to_txt('BotData.txt',stock_code_list)
    stock_code_list = Read_from_txt(fileName = 'BotData.txt')
    stock_code_list = get_stock_With_3Buy(stock_code_list = stock_code_list,AnaCycle = '5',begindate=FM3B_SD,enddate=FM3B_ED)
    Write_STo_Excel(FilePath ,stock_code_list,'StockList')

#选股策略五：选择30分钟可能出现三买的股票，条件为最后一笔方向为下，且价格在于GG/ZG,其中要求数据已经存储在相应文件目录中
def Sel_TMB_in_Pro(FilePath='FilePath',toldays = 'toldays',AnaCycle = '30',proDay = '2016-03-08'):
#    proDay = get_Trday_of_day(toldays,AnaCycle)
    FilePath2 = FilePath + '\\'+proDay+'\\'+ '沪深300成份股有交易'+AnaCycle+'.xls'
    df_stockcode = Get_TrdData_FromExcel(FilePath2,'权重排序')
    irows = 0
    totalrows = len(df_stockcode)
    df_stockcode['三买进行中'] = 0
    df_stockcode['最后笔方向'] = '无'
    df_stockcode['最后笔天数'] = '无'
    df_stockcode['前一笔力度'] = '无'
    while(irows < totalrows):
        stockcode = df_stockcode.loc[irows,'stockcode']
        stockcode = codeType(stockcode)
        print(stockcode)
        FilePath2 = FilePath + '\\'+proDay+'\\'+stockcode+AnaCycle+'.xls'
        sheetname = AnaCycle + 'Bi'
        Bi_Data = Get_TrdData_FromExcel(FilePath2,sheetname)
        totalrows2 = len(Bi_Data)
        LastBiDir = Bi_Data.loc[totalrows2-1,'Direc']
        LasBiDays = Bi_Data.loc[totalrows2-1,'TrDays']
        preBiLidu = Bi_Data.loc[totalrows2-2,'Lidu']
        preBiHilow = Bi_Data.loc[totalrows2-2,'HiLow']
        preIdenBiEndPrice = Bi_Data.loc[totalrows2-3,'endPrice']
        LastBiEndPrice = Bi_Data.loc[totalrows2-1,'endPrice']
        df_stockcode.loc[irows,'最后笔方向']  = LastBiDir
        df_stockcode.loc[irows,'最后笔天数']  = LasBiDays
        df_stockcode.loc[irows,'前一笔力度'] = preBiHilow + preBiLidu
        if(LastBiDir != '下'):
            irows = irows + 1
        else:
            BiCounter = len(Bi_Data)
            if(BiCounter < 3):
                irows = irows + 1
            else:
                Pivot_Data = BiPivot(Bi_Data)
                ZSExist,zs_data = ZhongShu(Pivot_Data)
                if(ZSExist == True):
                    LastBiEndPrice = Bi_Data.loc[totalrows2-1,'endPrice']
                    GG = zs_data['GG']
                    ZG = zs_data['ZG']
                    if(preIdenBiEndPrice<ZG):
                        if(LastBiEndPrice > GG):
                            df_stockcode.loc[irows,'三买进行中'] = 2
                            print(stockcode)
#                            BiPlot(Bi_Data)
                        elif(LastBiEndPrice > ZG):
                            df_stockcode.loc[irows,'三买进行中'] = 1
                            print(stockcode)
#                            BiPlot(Bi_Data)
                else:
                    df_stockcode.loc[irows,'三买进行中'] = -1
                irows = irows + 1
        df_stockcode = df_stockcode.sort_values(by='三买进行中',ascending=False)
        df_stockcode = ReIndex(df_stockcode)
        FilePath3 = FilePath  + '\\'+proDay+'\\'+ '沪深300三买统计'+AnaCycle+'.xlsx'
        Write_DF_T0_Excel(FilePath3,df_stockcode,sheetname)

        S_Trd_Data = Get_TrdData_FromExcel(FilePath2,'OriData')

        Inclu_Data = Include(S_Trd_Data)
        IniFX_Data = AllFX(Inclu_Data)
        RealFX_Data = TopBottomDistin(IniFX_Data)
        Bi_Data,BiCounter = Bee(RealFX_Data)
        Bi_Data = Bee_Update(Bi_Data,Inclu_Data)
        Bi_Data = Bee_TLidu(Bi_Data,S_Trd_Data)
        Bi_Data = Bee_LLidu(Bi_Data,S_Trd_Data)
        writer = ExcelWriter(FilePath2)
        S_Trd_Data.to_excel(writer,'OriData')
        Bi_Data.to_excel(writer,sheetname)
        writer.save()
        irows = irows + 1

#选股策略六，寻找日线上存在二买的股票
def Sel_SecB_in_Pro(FilePath='FilePath',toldays = 'toldays',AnaCycle = 'D',proDay = '2016-03-08'):
#    proDay = get_Trday_of_day(toldays,AnaCycle)
    FilePath2 = FilePath + '\\'+proDay+'\\'+ '沪深300成份股有交易'+AnaCycle+'.xls'
    df_stockcode = Get_TrdData_FromExcel(FilePath2,'权重排序')
    irows = 0
    totalrows = len(df_stockcode)
    df_stockcode['二买进行中'] = 0
    df_stockcode['最后笔方向'] = '无'
    df_stockcode['最后笔天数'] = '无'
    df_stockcode['前一笔力度'] = '无'
    while(irows < totalrows):
        stockcode = df_stockcode.loc[irows,'stockcode']
        stockcode = codeType(stockcode)
        print(stockcode)
        FilePath2 = FilePath + '\\'+proDay+'\\'+stockcode+AnaCycle+'.xls'
        sheetname = AnaCycle + 'Bi'
        Bi_Data = Get_TrdData_FromExcel(FilePath2,sheetname)
        totalrows2 = len(Bi_Data)
        LastBiDir = Bi_Data.loc[totalrows2-1,'Direc']
        LasBiDays = Bi_Data.loc[totalrows2-1,'TrDays']
        LastBiHilow = Bi_Data.loc[totalrows2-1,'HiLow']
        preBiEndPrice = Bi_Data.loc[totalrows2-2,'endPrice']
        preIdenBiEndPrice = Bi_Data.loc[totalrows2-3,'endPrice']
        LastBiEndPrice = Bi_Data.loc[totalrows2-1,'endPrice']
        LastBiLidu = Bi_Data.loc[totalrows2-1,'Lidu']
        pre3BiEndPrice = Bi_Data.loc[totalrows2-4,'endPrice']
        df_stockcode.loc[irows,'最后笔方向']  = LastBiDir
        df_stockcode.loc[irows,'最后笔天数']  = LasBiDays
        df_stockcode.loc[irows,'最后笔力度']  = LastBiLidu
        df_stockcode.loc[irows,'最后笔高低']  = LastBiHilow
        if(LastBiDir != '下'):
            irows = irows + 1
        else:
            BiCounter = len(Bi_Data)
            if(BiCounter < 3):
                irows = irows + 1
            else:
                Pivot_Data = BiPivot(Bi_Data)
                ZSExist,zs_data = ZhongShu(Pivot_Data)
                if(ZSExist == True):
                    DD = zs_data['DD']
                    GG = zs_data['GG']
                    ZG = zs_data['ZG']
                    ZD = zs_data['ZD']
                    if(preIdenBiEndPrice<DD) and (pre3BiEndPrice>DD): #后一个条件可有可没有
                        if(LastBiLidu == '弱') or (LastBiHilow =='高') or (Last_Value_inCol=='前包'):
                            if(preBiEndPrice > GG):
                                df_stockcode.loc[irows,'二买进行中'] = 3
                                print(stockcode)
#                                BiPlot(Bi_Data)
                            elif(LastBiEndPrice > ZG):
                                df_stockcode.loc[irows,'二买进行中'] = 2
                                print(stockcode)
#                                BiPlot(Bi_Data)
                            else:
                                df_stockcode.loc[irows,'二买进行中'] = 1
                                print(stockcode)
 #                               BiPlot(Bi_Data)
                    irows = irows + 1
                else:
                    df_stockcode.loc[irows,'二买进行中'] = -1
                    irows = irows + 1
        df_stockcode = df_stockcode.sort_values(by='二买进行中',ascending=False)
        df_stockcode = ReIndex(df_stockcode)
        FilePath3 = FilePath  + '\\'+proDay+'\\'+ '沪深300二买统计'+AnaCycle+'.xlsx'
        Write_DF_T0_Excel(FilePath3,df_stockcode,sheetname)




'''
#选股策略三：30分钟出现三买的股票，出于效率的考虑，先用最近一个交易日出现30分钟底分型，再判断15个交易日内，30分钟出现三买
# ，逻辑有问题，先行屏蔽
def Sel_TM_3B(n=0):
    DBot_SD = get_Trday_of_day(n+1)
    DBot_ED = get_Trday_of_day(n+0)
    TMPB_SD = get_Trday_of_day(n+15)
    TMPB_ED = get_Trday_of_day(8*n,'30')
    Sel_TM3B(DBot_SD,DBot_ED,TMPB_SD,TMPB_ED)

def Sel_TM3B(DBot_SD,DBot_ED,TMPB_SD,TMPB_ED):
    enddate = DBot_ED
    FilePath = 'D:\Chan Data\Selected Stock\Str3\Date'+enddate+ '.xls'
#    stock_code_list = get_all_stock()
    stock_code_list = get_hs300stock()
#    stock_code_list = get_stock_end_bot(stock_code_list = stock_code_list,begindate =DBot_SD, enddate = DBot_ED,AnaCycle='30')
#    Write_to_txt('BotData.txt',stock_code_list)
#    stock_code_list = Read_from_txt(fileName = 'BotData.txt')
    stock_code_list = get_stock_With_3Buy(stock_code_list = stock_code_list,AnaCycle = '30',begindate=TMPB_SD,enddate=TMPB_ED)
    Write_to_txt('3B.txt',stock_code_list)
    stock_code_list.append('sh')
    stock_code_list.append('sz')
    Write_STo_Excel(FilePath,stock_code_list,'StockList')
    return stock_code_list
'''

#选股策略4，n日来创tol个交易日以来新低，且30分钟下低弱(经典盘背)，当下处于中枢离开段且与中枢进入段背离（尚未实现）
def Sel_XD_PB(n=0,tol = 30, rec = 3):
    TMPB_SD = get_Trday_of_day(n+15)
    TMPB_ED = get_Trday_of_day(n)
    XD_SD = get_Trday_of_day(n + tol)
    XD_ED = get_Trday_of_day(n)
    Sel_XDPB(XD_SD,XD_ED,TMPB_SD,TMPB_ED,rec)

def Sel_XDPB(XD_SD='XD_SD',XD_ED='XD_ED',TMPB_SD='TMPB_SD',TMPB_ED='TMPB_ED',rec =3):
    startDate = XD_SD
    enddate = XD_ED
    FilePath = 'D:\Chan Data\Selected Stock\Str4\Date'+enddate+ '.xls'
    stock_code_list = get_all_stock()
    stock_code_list=Get_LowStock(stock_code_list,startDate,enddate,rec)
    Write_to_txt('XinDi.txt',stock_code_list)
    stock_code_list = Read_from_txt('XinDi.txt')
    stock_code_list = get_stock_panbeiCla(stock_code_list=stock_code_list,AnaCycle='30',begindate=TMPB_SD,enddate=TMPB_ED,Dir='下')
    Write_to_txt('PanBei.txt',stock_code_list)
    stock_code_list = Read_from_txt('PanBei.txt')
    Write_STo_Excel(FilePath,stock_code_list)

#大盘走势统计程序,统计与中枢位置关系,这里统计沪深300
def ZSWZ_Stat_300(n=0,AnaCycle='D'):
    stock_code_list = get_hs300stockOp()
    startDate = get_Trday_of_day(n+120)
    endDate = get_Trday_of_day(n)
    ZSWZ1 = Series([0,0,0],['上','中','下'])
    ZSWZ2 = Series([0,0,0,0,0,0],['上上','上下','中上','中下','下上','下下'])
    ZSWZ3 = Series([0,0,0,0,0],['GG之上','ZG与GG之间','中枢中','DD与ZD之间','DD之下'])
    DXQD = Series([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],['上高强','上高弱','上低强','上低弱','上前包强','上前包弱',
                '上后包强','上后包弱','下高强','下高弱','下低强','下低弱','下前包强','下前包弱','下后包强','下后包弱'])
    totalrows = len(stock_code_list)
    irows = 0
    while(irows < totalrows):
        stockcode = stock_code_list.loc[irows,'stockcode']
        stockcode = codeType(stockcode)
        zs_data,ZSR1,ZSR2,Pivot_Data = ZS_WZR(stockcode,AnaCycle,startDate,endDate)
        totalBi = len(Pivot_Data)
        Dir = Pivot_Data.loc[totalBi-1,'Direc']
        Hilow = Pivot_Data.loc[totalBi-1,'HiLow']
        Lidu = Pivot_Data.loc[totalBi-1,'Lidu']
        if(ZSR1=='上'):
            ZSWZ1['上'] =  ZSWZ1['上'] + 1
        elif(ZSR1=='中'):
            ZSWZ1['中'] =  ZSWZ1['中'] + 1
        elif(ZSR1=='下'):
            ZSWZ1['下'] =  ZSWZ1['下'] + 1
        if(ZSR2 =='GG之上'):
            ZSWZ3[ZSR2] = ZSWZ3[ZSR2] + 1
        elif(ZSR2 =='ZG与GG之间'):
            ZSWZ3[ZSR2] = ZSWZ3[ZSR2] + 1
        elif(ZSR2 =='中枢中'):
            ZSWZ3[ZSR2] = ZSWZ3[ZSR2] + 1
        elif(ZSR2 =='DD与ZD之间'):
            ZSWZ3[ZSR2] = ZSWZ3[ZSR2] + 1
        elif(ZSR2 =='DD之下'):
            ZSWZ3[ZSR2] = ZSWZ3[ZSR2] + 1
        Index1 = Dir + Hilow + Lidu
        DXQD[Index1] = DXQD[Index1] + 1
        if(ZSR1!='无') and(Dir!='无'):
            Index2 = ZSR1 + Dir
            ZSWZ2[Index2] = ZSWZ2[Index2] + 1
        irows = irows + 1
    date = get_Trday_of_day(0)
    FilePath = 'D:\Chan Data\MrkStat'+'\\'+date+'\\'+ '中枢关系.xls'
    FilePath2 ='D:\Chan Data\MrkStat'+'\\'+date+'\\'+ '当下强度.xls'
    FilePath3 ='D:\Chan Data\MrkStat'+'\\'+date+'\\'+ '位置方向.xls'
    FilePath4 ='D:\Chan Data\MrkStat'+'\\'+date+'\\'+ '中枢位置.xls'
    Write_STo_Excel(FilePath,ZSWZ1,'与中枢关系')
    Write_STo_Excel(FilePath2,DXQD,'当下强度')
    Write_STo_Excel(FilePath3,ZSWZ2,'位置方向')
    Write_STo_Excel(FilePath4,ZSWZ3,'中枢位置')
#    zs_gx_data = Series(zs_data.values,ZSR1,ZSR2,columns =['','','',])






















