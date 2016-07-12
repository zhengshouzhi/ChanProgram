# -*- coding: utf-8 -*-
#处理交易数据的函数，数据从DataInter调取
from DataInter import *
import pandas as pd
import numpy as np
from pandas import Series, DataFrame
import datetime as dt
from GenProcess import *
#取得要处理的源数据

#处理K线之间的包含关系，目前还是根据包含关系两出现前的两根线的方向确定方向，出于对行情的更仔细把握，用前几根K线的子趋势更好，不是
#很耽误应用，回头再改，或者保留原样。
def Include(SourceData = 'Trd_Data'):
    totaltrd_Days = len(SourceData.index)
    iDay = 1
    TrendStatus = 0
    #python的索引是0开始，因此结束为totaltrd_Days -1,找到第一个子趋势，以确定其前后的包含关系是近上涨还是下跌做包含处理
    for iday in range (1, totaltrd_Days ):
        YesDayPriceLow = SourceData.loc[iday-1,'low']
        YesDayPriceHigh = SourceData.loc[iday-1,'high']
        TodayPriceLow = SourceData.loc[iday,'low']
        TodayPriceHigh = SourceData.loc[iday,'high']
        if (YesDayPriceLow < TodayPriceLow) and (YesDayPriceHigh < TodayPriceHigh) :
            TrendStatus = 1
            break
        elif (YesDayPriceLow > TodayPriceLow) and (YesDayPriceHigh > TodayPriceHigh) :
            TrendStatus = -1
            break
        else:
            iday = iday + 1
    #iday是源数据表的索引，iIncday是包含处理后的数据索引
    iday = 1
    iIncday = 0
    #将源数据表的第一条交易数据拷贝到包含数据表，其中包含数据表为与源数据表地址不同的新数据表
    new_columns = ['date','open','high','low','close','volume']
    s =SourceData.iloc[iIncday]
    Inclu_Data = DataFrame(s)
    Inclu_Data = Inclu_Data.T

    for iday in range (1, totaltrd_Days):
        YesDayPriceLow = Inclu_Data.loc[iIncday,'low']
        YesDayPriceHigh = Inclu_Data.loc[iIncday,'high']
        TodayPriceLow = SourceData.loc[iday,'low']
        TodayPriceHigh = SourceData.loc[iday,'high']
        curDate = Inclu_Data.loc[iIncday,'date'] #已经处理后进入Include表的日期，不是当下处理的Today日期
        s =SourceData.iloc[iday]
        if (YesDayPriceLow < TodayPriceLow) and (YesDayPriceHigh < TodayPriceHigh):
            CurrInStatus = 1
            TrendStatus = CurrInStatus
            TrendStatus = CurrInStatus
            Inclu_Data = Inclu_Data.append(s,ignore_index = True)
            iday = iday + 1
            iIncday = iIncday + 1
        elif (YesDayPriceLow > TodayPriceLow) and (YesDayPriceHigh > TodayPriceHigh):
            CurrInStatus = -1
            TrendStatus = CurrInStatus
            Inclu_Data = Inclu_Data.append(s,ignore_index = True)
            iday = iday + 1
            iIncday = iIncday + 1
        else:
            CurrInStatus = 0
            #上升取低点的高点，高点的高点，日期取高点产生日的日期
            if (TrendStatus == 1) :
                if (YesDayPriceLow < TodayPriceLow):
                    YesDayPriceLow = TodayPriceLow
                if (YesDayPriceHigh < TodayPriceHigh):
                    YesDayPriceHigh = TodayPriceHigh
                    curDate = SourceData.loc[iday,'date']
            elif (TrendStatus == -1):
                if (YesDayPriceLow > TodayPriceLow) :
                    YesDayPriceLow = TodayPriceLow
                    curDate = SourceData.loc[iday,'date']
                if (YesDayPriceHigh > TodayPriceHigh):
                    YesDayPriceHigh = TodayPriceHigh
            #包含处理后，将包含后的值拷贝到饮食数据的最后一行
            Inclu_Data.loc[iIncday,'low'] = YesDayPriceLow
            Inclu_Data.loc[iIncday,'high'] = YesDayPriceHigh
            Inclu_Data.loc[iIncday,'date'] = curDate
            iday = iday + 1
    return Inclu_Data

#识别交易数据中的所有分型
def AllFX (Inclu_Data = 'Inclu_Data'):
    totalrows = len(Inclu_Data.index)
    totalcols = len(Inclu_Data.columns)
    #用即可，不修改，算是对重新编程的一点纪念
    Inclu_Data.insert(totalcols,'FenXing',value = Inclu_Data['low'])
    irows = 1
    #先默认所有的分型都不成立，顶分型为1，底分型为-1，第一个交易日和最后一个交易日不可能有成立的分型
    Inclu_Data.loc[irows -1 ,'FenXing'] = 0
    for irows in range(1,totalrows - 1 ):
        curFX = WhatFX(Inclu_Data,irows)
        Inclu_Data.loc[irows ,'FenXing'] = curFX
    Inclu_Data.loc[totalrows - 1 ,'FenXing'] = 0  #最后一行，不可能出现成立的分型。
    return Inclu_Data

#给出包含处理后的数据以及交易数据所属行数，返回当下所处的分型类型，顶分型为1，底分型为-1，非分型为0
def WhatFX(Inclu_Data = 'Inclu_Data', irows = 1):
    PriceHigh = Inclu_Data.loc[irows,'high']
    PriceLow = Inclu_Data.loc[irows,'low']
    prePriceHigh = Inclu_Data.loc[irows - 1,'high']
    prePriceLow = Inclu_Data.loc[irows - 1 ,'low']
    nxtPriceHigh = Inclu_Data.loc[irows + 1,'high']
    nxtPriceLow = Inclu_Data.loc[irows + 1 ,'low']
    curFX = 0
    if (PriceHigh > nxtPriceHigh) and (PriceLow > nxtPriceLow) and (PriceLow > nxtPriceLow) and (PriceLow > prePriceLow):
        curFX = 1
    elif (PriceHigh < prePriceHigh) and (PriceLow < prePriceLow) and (PriceLow < nxtPriceLow) and (PriceLow < nxtPriceLow):
        curFX = -1
    return curFX

#区分现有的分型是否成立, 另插入一列IsFX,成立为1，不成立为0，不确定为-1
def TopBottomDistin(IniFX_Data = 'IniFX_Data'):
    totalrows = len(IniFX_Data.index)
    totalcols = len(IniFX_Data.columns)
    IniFX_Data.insert(totalcols,'IsFX',value = IniFX_Data['FenXing'])
    curPassFX = 0
    curPassedrow = 0
    irows = 0
    # 原来用curpass == 0,这样的做法，在数据短或极端情况时，容易死循环，也即至数据终结没有成立的分型时，
    # 判断语句次序安排是出于节省计算的角度
    while (irows < totalrows-1  ):
        curFX = IniFX_Data.loc[irows, 'FenXing']
        if (curFX == 0):
            irows = irows + 1
            IniFX_Data.loc[irows, 'IsFX'] = 0
        #根据顶连着底，底连着顶的原则，如果当下分开型与前一成立分型同样类型，当下分型不能成立
        elif(curFX == curPassFX ):
                IniFX_Data.loc[irows, 'IsFX'] = 0
                irows = irows + 1
            #当下有成立分型，且当下分型与在先成立的分型不同
        elif (curPassFX != 0):
        #else中包含两种条件，一种是与前分型不相等，一种是目前还没有成立的分型（curPassFX = 0）
        #与当下成立分型之间不存在三根K线,分型不成立
            if(irows - curPassedrow <= 3):
                IniFX_Data.loc[irows, 'IsFX'] = 0
                irows = irows + 1
            else:
                IsFenXing = IsFX(IniFX_Data,irows)
                if (IsFenXing == 1) :
                    curPassFX = curFX
                    curPassedrow = irows
                    IniFX_Data.loc[irows, 'IsFX'] = 1
                    irows = irows + 1
                elif (IsFenXing == 0):
                    IniFX_Data.loc[irows, 'IsFX'] = 0
                    irows = irows + 1
                elif (IsFenXing == -1):
                    IniFX_Data.loc[irows, 'IsFX'] = -1
                    irows = irows + 1
        #处理curPassFX==0，即目前没有分型成立的情况，
        else:
                IsFenXing = IsFX(IniFX_Data,irows)
                if (IsFenXing == 1) :
                    curPassFX = curFX
                    curPassedrow = irows
                    IniFX_Data.loc[irows, 'IsFX'] = 1
                    irows = irows + 1
                elif (IsFenXing == 0):
                    IniFX_Data.loc[irows, 'IsFX'] = 0
                    irows = irows + 1
                elif (IsFenXing == -1):
                    IniFX_Data.loc[irows, 'IsFX'] = -1
                    irows = irows + 1
    #在最后一个确认成立的分型后，重新处理分型的未知成立与否关系
    irows = LastFXrow(IniFX_Data)
    while(irows < totalrows-1):
        IsFenXing = IsFX(IniFX_Data,irows)
        if(IsFenXing ==1) or(IsFenXing == -1):
            IniFX_Data.loc[irows, 'IsFX']  = -1
        irows = irows + 1

    #找到第一个成立的分型，并通过它新建DataFrame，其后成立的分型用append加入到RealFX_Data表中。
    FX_Colums = ['date','open','high','low','close','volume','FenXing','IsFX']
    totalrows = len(IniFX_Data.index)
    irows = 0
    while(irows < totalrows ):
        curFX = IniFX_Data.loc[irows,'FenXing']
        realFX = IniFX_Data.loc[irows,'IsFX']
        if (curFX != 0) and (realFX != 0):
            RealFX_Data = DataFrame(IniFX_Data.loc[irows],columns = FX_Colums )
            break
        irows = irows + 1
    irows = 0
    while(irows < totalrows - 1):
        curFX = IniFX_Data.loc[irows,'FenXing']
        IsFenXing = IniFX_Data.loc[irows,'IsFX']
        if (curFX != 0) and (IsFenXing != 0):
            s = IniFX_Data.loc[irows]
            RealFX_Data=RealFX_Data.append(s,ignore_index = True)
        irows = irows + 1
    RealFX_Data = RealFX_ErDup(RealFX_Data)
    return RealFX_Data
#RealFX_Data去重，非确定成立的数据，如果顶连着顶，选择高的顶，如果底连着底，选择低的底
def RealFX_ErDup(RealFX_Data ='RealFX_Data'):
    irows = LastFXrow(RealFX_Data)
    totalrows = len(RealFX_Data)
    while(irows < totalrows-1):
        if(RealFX_Data.loc[irows,'FenXing']==RealFX_Data.loc[irows+1,'FenXing']):
            RealFX_Data = RealFX_Data.drop(irows + 1)
            RealFX_Data = ReIndex(RealFX_Data)
            totalrows = totalrows -1
        else:
            irows = irows + 1
    return RealFX_Data

#返回最后一个分型对应的行号，复用于处理IniFX_Data和RealFX_Data
def LastFXrow(FX_Data='IniFX_Data'):
    totalrows = len(FX_Data)
    irows = totalrows -1
    while(irows >= 0):
        if(FX_Data.loc[irows, 'IsFX']==1):
            break
        else:
            irows = irows -1
    if(irows == 0) and (FX_Data.loc[irows, 'IsFX'] != 1):
        irows = -1 #此处本来返回-1,表示无成立分开，出于程序运行原因，改为0
    if(irows ==-1):
        irows = 0
    return irows



#判断分型是否成立的函数，成立返回1,不成立返回0，因后续数据不足不确定返回-1
#顶分型成立的逻辑在于与下一底分型的距离超过3（有一根自由K线），以顶分型开始，顶分型高点大于
#底分型高点，或以底分型开始，底分型低点低于顶分型低点。
#以顶分型开始为例，顶底距离小于3时，如果当下顶高于下一顶，则当下顶成立，这里如果下一顶对应的底的高点高于当下顶的
#高点，可能出现意外，这种意外对小周期操作可能有影响，此处不遵守经典缠论，预估应该有利于分析，具体等问题出现时再分析（初始记录）
#记录更新，要求对应顶的底满足，顶高点>底高点and项低点>底低点
#当下一分型还未生成时，IsFenXing = -1
#已经出现意外，以顶分型开始为例，顶底距离小于3时，如果当下顶高于下一顶，则继续考虑当下顶与下下底是否构成笔，极端情况1，-1，1.-1.
#与下下底距离也小于3，则考虑与第3个底是否成立。
def IsFX (IniFX_Data = 'IniFX_Data', irows = 0):
    IsFenXing = 0
    curFX = IniFX_Data.loc[irows,'FenXing']
    if (curFX == 1):
        disNextoppFX = NextoppFX(IniFX_Data, irows)  #下一底分型距离，下一顶分型距离
        disNextBtoTop = NextoppFX(IniFX_Data, irows + disNextoppFX + 1 ) #下一底分型与下一顶分型距离
        disNextIdenFX = NextidenFX(IniFX_Data, irows) #下一顶分型距离
        #不存在下一底分型或顶分型，不能判断分型是否成立
        if (disNextoppFX == -1) or (disNextBtoTop == -1):
            IsFenXing = -1
        # 当前顶分型与底分型距离大于等于3，下一底分型与一下顶分型距离大于等于3
        elif (disNextoppFX >= 3) and (disNextBtoTop>=3):
            #顶分型高点高于对应底分型的高点
            curFXHigh = FXHigh(IniFX_Data,irows)
            nxtoppFXHigh = FXHigh(IniFX_Data,irows + disNextoppFX + 1)
            curFXLow = FXLow(IniFX_Data,irows)
            nxtoppFXLow = FXLow(IniFX_Data,irows + disNextoppFX + 1)
            if (curFXHigh > nxtoppFXHigh) and (curFXLow > nxtoppFXLow):
                IsFenXing = 1
        #顶底分型距离大于3，下一底与下一顶距离小于3
        elif(disNextoppFX >= 3) and (disNextBtoTop <3):
            curFXHigh = FXHigh(IniFX_Data,irows)
            nxtoppFXHigh = FXHigh(IniFX_Data, irows + disNextoppFX + 1)
            nxtIdenFXHigh = FXHigh(IniFX_Data,irows + disNextIdenFX + 1)
            #如果与顶分型相对应的底分型距离大于3，底分型离下一顶分型小于3，且下一顶分型更高，则当下顶分型不成立
            if (curFXHigh > nxtoppFXHigh) and(curFXHigh > nxtIdenFXHigh):
                IsFenXing = 1
        else: #处理下一底分型与顶分型距离小于3的情况
            #与一下顶分型距离
            disNextidenFX = NextidenFX(IniFX_Data,irows)
            if(disNextidenFX != -1):
                curFXHigh = FXHigh(IniFX_Data,irows)
                nxtidenFXHigh = FXHigh(IniFX_Data,irows + disNextidenFX + 1)
                #顶分型高于下一个顶分型分型有成立可能性，如果低于则顶分型不成立。
                if (curFXHigh > nxtidenFXHigh):
                    #下个顶分型与下下个底分型距离，从而得到当下顶分型与下下个底分型的距离
                    disNNextoppFX = disFX(IniFX_Data,irows,-1,2)
                    #与下下底分型距离大于等于3，能构成一笔
                    if (disNNextoppFX >= 3):
                        curFXHigh = FXHigh(IniFX_Data,irows) #i当下顶分型高点
                        nnxtoppFXHigh = FXHigh(IniFX_Data, irows + disNNextoppFX + 1) #下下底分型高点
                        disNNextIdenFXpart3 = NextoppFX(IniFX_Data, irows + disNNextoppFX + 1)
                        disNNextIdenFX = disNNextoppFX + disNNextIdenFXpart3 + 1
                        #下下顶分型高点
                        nnxtIdenFXHigh = FXHigh(IniFX_Data, irows + disNNextIdenFX + 1)
                        if(disNNextIdenFXpart3 == -1):
                            IsFenXing = -1
                        elif(disNNextIdenFXpart3 >= 3):
                            IsFenXing = 1
                        elif (curFXHigh > nnxtoppFXHigh) and (curFXHigh >nnxtIdenFXHigh):
                            IsFenXing = 1
                    elif (disNextoppFX == -1):
                            IsFenXing = -1
                    #比第三个顶分型高，当下顶分型成立，没有再判断是否大于3主要因为即使分型间距离都是0，当下顶与第二底距离也必然大于3
                    #此时，先判断
                    else:
                        #如果第三个底分型和第三个顶分型之间距离大于等于3，则当前顶分型成立（目前未加入当前顶分型高于第三个底分型高点的
                        # 限制条件，是否加入，根据测试结果再考虑，纠结的行情中，为表现当时的重价空间，不加入可能也是合理的。
                        dis0to3OppFx = disFX(IniFX_Data,irows,-1,3)
                        dis0to3IdenFx = disFX(IniFX_Data,irows,1,3)
                        disb3top3 = dis0to3IdenFx - dis0to3OppFx -1
                        if (dis0to3OppFx == -1) or(dis0to3IdenFx == -1):
                            IsFenXing = -1
                        elif(disb3top3 >= 3):
                            curFXHigh = FXHigh(IniFX_Data,irows)
                            curFXLow = FXHigh(IniFX_Data,irows)
                            thirdOppFXHigh = FXHigh(IniFX_Data,irows + dis0to3OppFx + 1)
                            thirdOppFXLow = FXHigh(IniFX_Data,irows + dis0to3OppFx + 1)
                            if(curFXHigh > thirdOppFXHigh) and (curFXLow > thirdOppFXLow):
                                IsFenXing = 1
                        else:
                            curFXHigh = FXHigh(IniFX_Data,irows) #i当下顶分型高点
                            disNNextIdenFX = disFX(IniFX_Data,irows,1,2)
                            thirdOppFXHigh = FXHigh(IniFX_Data,irows + dis0to3OppFx + 1)
                            secondIdenFXHigh = FXHigh(IniFX_Data,irows + disNNextIdenFX + 1)
                            thirdidenFXHigh = FXHigh(IniFX_Data,irows + dis0to3IdenFx + 1)
                            curFXLow = FXHigh(IniFX_Data,irows)
                            thirdOppFXLow = FXHigh(IniFX_Data,irows + dis0to3OppFx + 1)
                            if(curFXHigh > thirdidenFXHigh) and (curFXHigh > secondIdenFXHigh) and\
                                    (curFXHigh > thirdOppFXHigh) and (curFXLow <thirdOppFXLow):
                                IsFenXing = 1
            else:
                 IsFenXing = -1
    elif (curFX == -1):
        #下一个顶分型距离，下下底分型距离
        disNextoppFX = NextoppFX(IniFX_Data, irows)
        disNextIdenFXpart3 = NextoppFX(IniFX_Data, irows + disNextoppFX + 1 )
        disNextIdenFX = NextidenFX(IniFX_Data, irows)
        if (disNextoppFX == -1) or (disNextIdenFXpart3 == -1):
            IsFenXing = -1
        elif (disNextoppFX >= 3) and (disNextIdenFXpart3>=3):
             curFXLow = FXLow(IniFX_Data,irows)
             nxtoppFXLow = FXLow(IniFX_Data,irows + disNextoppFX + 1)
             curFXHigh = FXHigh(IniFX_Data,irows)
             nxtoppFXHigh = FXHigh(IniFX_Data,irows + disNextoppFX + 1)
             if (curFXLow < nxtoppFXLow) and (curFXHigh < nxtoppFXHigh):
                 IsFenXing = 1
        elif(disNextoppFX >= 3) and (disNextIdenFXpart3 <3):
            curFXLow = FXLow(IniFX_Data,irows)
            nxtoppFXLow = FXLow(IniFX_Data, irows + disNextoppFX + 1)
            nxtIdenFXLow = FXLow(IniFX_Data,irows + disNextIdenFX + 1)
            if (curFXLow < nxtoppFXLow) and(curFXLow <nxtIdenFXLow):
                IsFenXing = 1
        else:
            disNextidenFX = NextidenFX(IniFX_Data,irows)
            if(disNextidenFX != -1):
                curFXLow = FXLow(IniFX_Data,irows)
                nxtidenFXLow = FXLow(IniFX_Data,irows + disNextidenFX + 1)
                if (curFXLow < nxtidenFXLow):
                    disNNextoppFXpart3 = NextoppFX(IniFX_Data, irows +  disNextidenFX + 1 )
                    disNNextoppFX = disNextidenFX + disNNextoppFXpart3 + 1
                    if (disNNextoppFX >= 3): #2代表之间的两个分型
                        curFXLow = FXLow(IniFX_Data,irows)
                        nnxtoppFXLow = FXLow(IniFX_Data,irows + disNNextoppFX + 1)
                        disNNextIdenFXpart3 = NextoppFX(IniFX_Data, irows + disNNextoppFX + 1)
                        disNNextIdenFX = disNNextoppFX + disNNextIdenFXpart3 + 1
                        nnxtIdenFXLow = FXLow(IniFX_Data, irows + disNNextIdenFX + 1)
                        if(disNNextIdenFXpart3 == -1):
                            IsFenXing = -1
                        if (curFXLow < nnxtoppFXLow) and (curFXLow < nnxtIdenFXLow):
                            IsFenXing = 1
                    elif (disNNextoppFX == -1): #下一个相反分型尚未产生
                            IsFenXing = -1
                    else:
                        #如果第三个底分型和第三个顶分型之间距离大于等于3，则当前顶分型成立（目前未加入当前顶分型高于第三个底分型高点的
                        # 限制条件，是否加入，根据测试结果再考虑，纠结的行情中，为表现当时的重价空间，不加入可能也是合理的。
                        dis0to3OppFx = disFX(IniFX_Data,irows,-1,3)
                        dis0to3IdenFx = disFX(IniFX_Data,irows,1,3)
                        dist3tob3 = dis0to3IdenFx - dis0to3OppFx -1
                        if (dis0to3OppFx == -1) or(dis0to3IdenFx == -1):
                            IsFenXing = -1
                        elif(dist3tob3 >= 3):
                            curFXLow = FXLow(IniFX_Data,irows) #i当下顶分型高点
                            curFXHigh = FXHigh(IniFX_Data,irows)
                            thirdOppFXHigh = FXHigh(IniFX_Data,irows + dis0to3OppFx + 1)
                            thirdOppFXLow = FXLow(IniFX_Data,irows + dis0to3OppFx + 1)
                            if(curFXLow <thirdOppFXLow ) and (curFXHigh < thirdOppFXHigh):
                                IsFenXing = 1
                        else:
                            curFXLow = FXLow(IniFX_Data,irows) #i当下顶分型高点
                            curFXHigh = FXHigh(IniFX_Data,irows)
                            disNNextIdenFX = disFX(IniFX_Data,irows,1,2)
                            secondIdenFXLow = FXLow(IniFX_Data,irows + disNNextIdenFX + 1)
                            thirdidenFXLow = FXLow(IniFX_Data,irows + dis0to3IdenFx + 1)
                            thirdOppFXHigh = FXHigh(IniFX_Data,irows + dis0to3OppFx + 1)
                            thirdOppFXLow = FXLow(IniFX_Data,irows + dis0to3OppFx + 1)
                            if(curFXLow < thirdidenFXLow) and (curFXLow < secondIdenFXLow) \
                                    and (curFXHigh < thirdOppFXHigh) and (curFXLow <thirdOppFXLow ):
                                IsFenXing = 1
            else:
                IsFenXing = -1
    else:
        IsFenXing = 0
    return  IsFenXing
#对于当下行（irows）给出的分型，根据给出的数量（counter）,求出与当下分型相同或相反的分型的距离，相同相反用IdenOpp表示，相同为1
#相反为-1,返回值为距离，如果交易数据不支撑导致
def disFX(IniFX_Data = 'IniFX_Data',irows = 0, IdenOpp = 1,counter = 1 ):
    totalrows = len(IniFX_Data.index)
    curFX = IniFX_Data.loc[irows,'FenXing']
    iFXcounter = 0  #
    iDiscounter = 0
    while(iFXcounter < counter):
        if(irows + iDiscounter + 1 < totalrows):
            nxtFX = IniFX_Data.loc[irows +iDiscounter + 1 ,'FenXing']
            if(IdenOpp ==1) and (nxtFX == curFX ):
                iFXcounter = iFXcounter + 1
                iDiscounter = iDiscounter + 1
            elif (IdenOpp ==-1) and (nxtFX == -curFX):
                iFXcounter = iFXcounter + 1
                iDiscounter = iDiscounter + 1
            else:
                iDiscounter = iDiscounter + 1
        else:
            return -1
    return iDiscounter-1

#计算与下一个相反分型的距离,如下一相反分型不存在（通常发生在后续交易还未发生），返回-1
def NextoppFX(IniFX_Data = 'IniFX_Data', irows =0):
    totalrows = len(IniFX_Data.index)
    curFX = IniFX_Data.loc[irows,'FenXing']
    icounter = 0
    if (irows + icounter + 1) < totalrows:
        nxtFX = IniFX_Data.loc[irows + icounter + 1,'FenXing']
    else:
        icounter = -1
    #循环直至相反分型出现
    while nxtFX != -curFX:
        if (icounter == -1):
            break
        icounter = icounter + 1
        if (irows + icounter + 1) < totalrows:
            nxtFX = IniFX_Data.loc[irows + icounter + 1,'FenXing']
        else:
            icounter = -1
    return icounter

#计算下一个相同分型距离
def NextidenFX(IniFX_Data = 'IniFX_Data', irows =0):
    totalrows = len(IniFX_Data.index)
    curFX = IniFX_Data.loc[irows,'FenXing']
    icounter = 0
    if (irows + icounter + 1) < totalrows:
        nxtFX = IniFX_Data.loc[irows + icounter + 1,'FenXing']
    else:
        icounter = -1
    #循环直至相同分型出现
    while nxtFX != curFX:
        if (icounter == -1):
            break
        icounter = icounter + 1
        if (irows + icounter + 1) < totalrows:
            nxtFX = IniFX_Data.loc[irows + icounter + 1,'FenXing']
        else:
            icounter = -1
    return icounter

#返回分型的最高点，顶分型，底分型都可以
def FXHigh(IniFX_Data = 'IniFX_Data', irows =0):
    highPri = 0
    curFX = IniFX_Data.loc[irows,'FenXing']
    if (curFX == 1):
        highPri = IniFX_Data.loc[irows,'high']
    elif (curFX == -1):
        if (IniFX_Data.loc[irows-1,'high'] > IniFX_Data.loc[irows + 1,'high'] ):
            highPri = IniFX_Data.loc[irows - 1,'high']
        else:
            highPri = IniFX_Data.loc[irows +1 ,'high']
    return highPri
#返回分型的最低点，顶分型，底分型都可以
def FXLow(IniFX_Data = 'IniFX_Data', irows =0):
    lowPri = 0
    curFX = IniFX_Data.loc[irows,'FenXing']
    if (curFX == -1):
        lowPri = IniFX_Data.loc[irows,'low']
    elif (curFX == 1):
        if (IniFX_Data.loc[irows-1,'low'] < IniFX_Data.loc[irows + 1,'low'] ):
            lowPri = IniFX_Data.loc[irows - 1,'low']
        else:
            lowPri = IniFX_Data.loc[irows +1 ,'low']
    return lowPri


#将分型列中的数据拷贝到笔,用小蜜蜂为名纯属个人喜好,当分型总数为1时，待处理，将尾值日期加入待处理
def Bee (RealFX_Data = 'RealFX_Data'):
    #笔的内容，开始日期、结束日期、起始价格、终止价格、交易日数、斜率、均量、方向（上下）、高低、力度（强度）
    bi_columns = ['startDate','endDate','startPrice','endPrice','Direc']
    totalrows = len(RealFX_Data.index)
    BiCounter  = 0
    if (totalrows <= 1):
        return None, 0
    elif(totalrows > 1):
        BiCounter = totalrows -1
        irows = 1
        curFX = RealFX_Data.loc[irows,'FenXing']
        endDate = RealFX_Data.loc[irows,'date']
        startDate = RealFX_Data.loc[irows-1,'date']
        #如果当下分型为顶分型，则当下笔为底-->顶，方向为‘上’，笔的开始价格为前分型低点，结束价格为当下分型高点；
        #如果当下分型为底分型，则当下笔为顶-->底，方向为‘下’，笔的开始价格为前分型高点，结束价格为当下分型低点。
        if curFX == 1:
            Direc = '上'
            startPrice =  RealFX_Data.loc[irows-1,'low']
            endPrice = RealFX_Data.loc[irows,'high']
        elif curFX == -1:
            Direc = '下'
            startPrice =  RealFX_Data.loc[irows-1,'high']
            endPrice = RealFX_Data.loc[irows,'low']
        #新建一个DataFrame,样例代码
        s = Series([startDate,endDate,startPrice,endPrice,Direc],index =  bi_columns)
        Bi_Data = DataFrame(s)
        Bi_Data = Bi_Data.T
        irows = irows + 1
        #通过成立的分型表生成笔数据表，并对
        while (irows < totalrows):
            curFX = RealFX_Data.loc[irows,'FenXing']
            endDate = RealFX_Data.loc[irows,'date']
            startDate = RealFX_Data.loc[irows-1,'date']
            IsFX = RealFX_Data.loc[irows,'IsFX']
            if (curFX == 1) : #删除and (IsFX != -1)，为分析方便，把未来不知道是否成立的分型也显示出来
                Direc = '上'
                startPrice =  RealFX_Data.loc[irows-1,'low']
                endPrice = RealFX_Data.loc[irows,'high']
            elif (curFX == -1) : #:删除and (IsFX != -1)，为分析方便，把未来不知道是否成立的分型也显示出来
                Direc = '下'
                startPrice =  RealFX_Data.loc[irows-1,'high']
                endPrice = RealFX_Data.loc[irows,'low']
            s = Series([startDate,endDate,startPrice,endPrice,Direc],index =  bi_columns)
            Bi_Data = Bi_Data.append(s,ignore_index = True)
            irows = irows + 1
    totalrows = len(Bi_Data)
    if(totalrows >= 2):
        Bi_Data = Bee_ErDup(Bi_Data)
        BiCounter = BiCounter -1
    return Bi_Data, BiCounter

#笔数据更新至最新笔，将最后一个分型（顶底）之后的数据，也即尚未有成立分型的笔加入笔数据中，使用处理。
def Bee_Update(Bi_Data = 'Bi_Data',S_Trd_Data ='S_Trd_Data'):
    totalrows = len(Bi_Data.index)
    totalDays = len(S_Trd_Data)
    #cur开头代表笔数据，last代表交易数据
    curBiDir = Bi_Data.loc[totalrows-1,'Direc']
    curBiEnd = Bi_Data.loc[totalrows-1,'endPrice']
    curBiStart = Bi_Data.loc[totalrows-1,'startPrice']
    lastPriceHigh = S_Trd_Data.loc[totalDays-1,'high']
    lastPriceLow = S_Trd_Data.loc[totalDays-1,'low']
    lastendDate = S_Trd_Data.loc[totalDays-1,'date']
    if (curBiDir =='上') and(curBiEnd < lastPriceHigh):
        Bi_Data.loc[totalrows-1,'endDate'] = lastendDate
        Bi_Data.loc[totalrows-1,'endPrice'] = lastPriceHigh
    elif (curBiDir =='下') and(curBiEnd > lastPriceLow):
        Bi_Data.loc[totalrows-1,'endDate'] = lastendDate
        Bi_Data.loc[totalrows-1,'endPrice'] = lastPriceLow
    else:
        bi_columns = ['startDate','endDate','startPrice','endPrice','Direc']
        startDate = Bi_Data.loc[totalrows-1,'endDate']
        startPrice = Bi_Data.loc[totalrows-1,'endPrice']
        endPrice =S_Trd_Data.loc[totalDays-1,'high']
        Direc = '上'
        if(curBiDir=='上'):
            Direc = '下'
            endPrice =S_Trd_Data.loc[totalDays-1,'low']
        s = Series([startDate,lastendDate,startPrice,endPrice,Direc],index =  bi_columns)
        Bi_Data = Bi_Data.append(s,ignore_index = True)
    totalrows = len(Bi_Data)
    if(totalrows >= 2):
        Bi_Data = Bee_ErDup(Bi_Data)
    #处理当下尚未形成顶分型，但当下最高价格高于前一个不确定顶的情况，待检验
    totalrows = len(Bi_Data)
    startDate = Bi_Data.loc[totalrows-2,'startDate']
    endDate = Bi_Data.loc[totalrows-2,'endDate']
    preTrdays = trdCount(S_Trd_Data,startDate,endDate)
    if(preTrdays < 5):
        lastBiDir = Bi_Data.loc[totalrows-1,'Direc']
        if(lastBiDir =='上'):
            if(Bi_Data.loc[totalrows-1,'endPrice'] > Bi_Data.loc[totalrows-3,'endPrice']):
                Bi_Data.loc[totalrows-1,'startDate'] = Bi_Data.loc[totalrows-3,'startDate']
                Bi_Data.loc[totalrows-1,'startPrice'] = Bi_Data.loc[totalrows-3,'startPrice']
                Bi_Data = Bi_Data.drop(totalrows-2)
                Bi_Data = Bi_Data.drop(totalrows-3)
                Bi_Data = ReIndex(Bi_Data)
        elif(lastBiDir =='下'):
            if(Bi_Data.loc[totalrows-1,'endPrice'] < Bi_Data.loc[totalrows-3,'endPrice']):
                Bi_Data.loc[totalrows-1,'startDate'] = Bi_Data.loc[totalrows-3,'startDate']
                Bi_Data.loc[totalrows-1,'startPrice'] = Bi_Data.loc[totalrows-3,'startPrice']
                Bi_Data = Bi_Data.drop(totalrows-2)
                Bi_Data = Bi_Data.drop(totalrows-3)
                Bi_Data = ReIndex(Bi_Data)
    '''
    totalrows = len(Bi_Data)
    if(totalrows >= 2):
        if(Bi_Data.loc[totalrows-2,'Direc']==Bi_Data.loc[totalrows-1,'Direc']):
            Bi_Data.loc[totalrows-2,'endDate']==Bi_Data.loc[totalrows-1,'endDate']
            Bi_Data.loc[totalrows-2,'endPrice']==Bi_Data.loc[totalrows-1,'endPrice']
            Bi_Data = Bi_Data.drop(totalrows-1)
    '''
    return Bi_Data

#笔数据去重，由于未确认是否成立分型都是用-1，因此，在结尾处可能有两条以上的同向笔，笔更新也可能有此情况，
# 因此需要去重,这个函数还有待检验
def Bee_ErDup(Bi_Data = 'Bi_Data'):
    totalrows = len(Bi_Data)
    curDir = Bi_Data.loc[totalrows-1,'Direc']
    preDir = Bi_Data.loc[totalrows-2,'Direc']
    curPrice = Bi_Data.loc[totalrows-1,'endPrice']
    prePrice = Bi_Data.loc[totalrows-2,'endPrice']
    curDate = Bi_Data.loc[totalrows-1,'endDate']
    if(curDir == '上')and (curDir == preDir):
        if(curPrice > prePrice):
            Bi_Data.loc[totalrows-2,'endPrice'] = curPrice
            Bi_Data.loc[totalrows-2,'endDate'] = curDate
        Bi_Data = Bi_Data.drop(totalrows-1)
    elif(curDir == '下')and (curDir == preDir):
        if(curPrice < prePrice):
            Bi_Data.loc[totalrows-2,'endPrice'] = curPrice
            Bi_Data.loc[totalrows-2,'endDate'] = curDate
        Bi_Data = Bi_Data.drop(totalrows-1)
    return Bi_Data
#笔的趋势力度,用斜率代表力度
def Bee_TLidu (Bi_Data = 'Bi_Data',SourceData = 'Trd_Data'):
    TrdCol = []
    XLCol = []
    totalrows = len(Bi_Data)
    irows = 0
    while (irows < totalrows):
        startPrice = Bi_Data.loc[irows,'startPrice']
        endPrice = Bi_Data.loc[irows,'endPrice']
        startDate = Bi_Data.loc[irows,'startDate']
        endDate = Bi_Data.loc[irows,'endDate']
        curDir = Bi_Data.loc[irows,'Direc']
        TrDays = trdCount(SourceData,startDate=startDate,endDate=endDate)
        XL = (endPrice - startPrice)*100/TrDays
        TrdCol.append(TrDays)
        XLCol.append(XL)
        irows = irows + 1
    totalcols = len(Bi_Data.columns)
    Bi_Data.insert(totalcols,'TrDays',value =TrdCol)
    totalcols = totalcols + 1
    Bi_Data.insert(totalcols,'XL',value =XLCol)
    irows = 0
    HiLowCol = []
    LiDuCol = []

    while (irows < totalrows ):
        if (irows >= 2):
            curDir = Bi_Data.loc[irows,'Direc']
            curXL = Bi_Data.loc[irows,'XL']
            preXL = Bi_Data.loc[irows-2,'XL']
            curStartPrice = Bi_Data.loc[irows,'startPrice']
            curEndPrice = Bi_Data.loc[irows,'endPrice']
            preStartPrice = Bi_Data.loc[irows-2,'startPrice']
            preEndPrice = Bi_Data.loc[irows-2,'endPrice']
            if (abs(curXL) > abs(preXL)):
                Lidu = '强'
            else:
                Lidu = '弱'
            if(curEndPrice > preEndPrice) and (curStartPrice > preStartPrice):
                HighLow = '高'
            elif(curEndPrice < preEndPrice) and (curStartPrice < preStartPrice):
                HighLow = '低'
            elif(curEndPrice <= preEndPrice) and (curStartPrice >= preStartPrice):
                if(curDir =='上'):
                    HighLow = '前包'
                elif(curDir =='下'):
                    HighLow = '后包'
            elif(curEndPrice >= preEndPrice) and (curStartPrice <= preStartPrice):
                if(curDir =='上'):
                    HighLow = '后包'
                elif(curDir =='下'):
                    HighLow = '前包'
            HiLowCol.append(HighLow)
            LiDuCol.append(Lidu)
            irows = irows + 1
        else:
            HiLowCol.append('无')
            LiDuCol.append('无')
            irows = irows + 1
    totalcols = len(Bi_Data.columns)
    Bi_Data.insert(totalcols,'HiLow',value =HiLowCol)
    totalcols = totalcols + 1
    Bi_Data.insert(totalcols,'Lidu',value =LiDuCol)
    return Bi_Data
#笔的量力度，考验各笔之间均量的增减
def Bee_LLidu(Bi_Data = 'Bi_Data',SourceData = 'Trd_Data'):
    TrVCol = []
    LLiduCol = []
    totalrows = len(Bi_Data)
    irows = 0
    while (irows < totalrows):
        startDate = Bi_Data.loc[irows,'startDate']
        endDate = Bi_Data.loc[irows,'endDate']
        TrVolume = trdVolume(SourceData,startDate=startDate,endDate=endDate)
        trDays = Bi_Data.loc[irows,'TrDays']
        JL = TrVolume/trDays
        TrVCol.append(JL)
        irows = irows + 1
    totalcols = len(Bi_Data.columns)
    Bi_Data.insert(totalcols,'JL',value =TrVCol)
    irows = 0
    LLiduCol = []
    while (irows < totalrows ):
        if (irows >= 2):
            curJL = Bi_Data.loc[irows,'JL']
            preJL = Bi_Data.loc[irows-2,'JL']
            if (abs(curJL) > abs(preJL)):
                LLidu = '增'
            else:
                LLidu = '减'
            LLiduCol.append(LLidu)
            irows = irows + 1
        else:
            LLiduCol.append('无')
            irows = irows + 1
    totalcols = len(Bi_Data.columns)
    Bi_Data.insert(totalcols,'LLidu',value =LLiduCol)
    return Bi_Data
# 笔的MACD力度，用上升笔和下降笔的MACD红、绿柱子这和代表力度
def Bee_BarLidu(Bi_Data = 'Bi_Data',SourceData = 'Trd_Data'):
    TrBCol = []
    totalrows = len(Bi_Data)
    irows = 0
    while (irows < totalrows):
        startDate = Bi_Data.loc[irows,'startDate']
        endDate = Bi_Data.loc[irows,'endDate']
        curDir = Bi_Data.loc[irows,'Direc']
        TrBar = trdBar(SourceData,startDate,endDate,curDir)
        TrBCol.append(TrBar)
        irows = irows + 1
    totalcols = len(Bi_Data.columns)
    Bi_Data.insert(totalcols,'totBar',value =TrBCol)
    irows = 0
    BarLiduCol = []
    while (irows < totalrows ):
        if (irows >= 2):
            curBar = Bi_Data.loc[irows,'totBar']
            preBar = Bi_Data.loc[irows-2,'totBar']
            if (abs(curBar) > abs(preBar)):
                BarLidu = '强'
            else:
                BarLidu = '弱'
            BarLiduCol.append(BarLidu)
            irows = irows + 1
        else:
            BarLiduCol.append('无')
            irows = irows + 1
    totalcols = len(Bi_Data.columns)
    Bi_Data.insert(totalcols,'BarLidu',value =BarLiduCol)
    return Bi_Data

#笔的MTI力度,MFI=(最高价-最低价)/交易量
def Bee_MFILidu (Bi_Data = 'Bi_Data',SourceData = 'Trd_Data'):
    MFICol = []
    totalrows = len(Bi_Data)
    irows = 0
    while (irows < totalrows):
        startDate = Bi_Data.loc[irows,'startDate']
        endDate = Bi_Data.loc[irows,'endDate']
        totaMFI = totalMFI(SourceData,startDate=startDate,endDate=endDate)
        trDays = trdCount(SourceData,startDate=startDate,endDate=endDate)
        MFI = totaMFI/trDays
        MFICol.append(MFI)
        irows = irows + 1
    totalcols = len(Bi_Data.columns)
    Bi_Data.insert(totalcols,'MFI',value =MFICol)
    irows = 0
    MFILiduCol = []
    while (irows < totalrows ):
        if (irows >= 2):
            curMFI = Bi_Data.loc[irows,'MFI']
            preMFI = Bi_Data.loc[irows-2,'MFI']
            if (abs(curMFI) > abs(preMFI)):
                MFILidu = '增'
            else:
                MFILidu = '减'
            MFILiduCol.append(MFILidu)
            irows = irows + 1
        else:
            MFILiduCol.append('无')
            irows = irows + 1
    totalcols = totalcols + 1
    Bi_Data.insert(totalcols,'MFILidu',value =MFILiduCol)
    return Bi_Data

#计算两日期间的交易日量,SourceData是原始交易数据（未包含处理）
def trdCount (SourceData = 'Trd_Data',startDate = '',endDate = ''):
    totalrows = len(SourceData.index)
    irows = 0
    curDate = (SourceData.loc[irows,'date'])
    iDayCounter = 0
    #此处停止执行时，日期调整至起始时间点
    while (curDate < startDate):
        irows = irows + 1
        curDate = SourceData.loc[irows,'date']
    while (curDate <= endDate):
        irows = irows + 1
        iDayCounter = iDayCounter + 1
        if(irows < totalrows):
            curDate = SourceData.loc[irows,'date']
        else:
            break
    return iDayCounter

#计算两个交易日之间的交易量
def trdVolume (SourceData = 'Trd_Data',startDate = '',endDate = ''):
    totalrows = len(SourceData.index)
    irows = 0
    curDate = (SourceData.loc[irows,'date'])
    trdVolume = 0
    #此处停止执行时，日期调整至起始时间点
    while (curDate < startDate):
        irows = irows + 1
        curDate = SourceData.loc[irows,'date']
    while (curDate <= endDate):
        curVolume = SourceData.loc[irows,'volume']
        irows = irows + 1
        trdVolume = trdVolume + curVolume
        if(irows < totalrows):
            curDate = SourceData.loc[irows,'date']
        else:
            break
    return trdVolume

#计算两个日期之间的MTI
def totalMFI (SourceData = 'Trd_Data',startDate = '',endDate = ''):
    totalrows = len(SourceData.index)
    irows = 0
    curDate = (SourceData.loc[irows,'date'])
    totalMFI = 0
    #此处停止执行时，日期调整至起始时间点
    while (curDate < startDate):
        irows = irows + 1
        curDate = SourceData.loc[irows,'date']
    while (curDate <= endDate):
        cuMTI = SourceData.loc[irows,'MFI']
        irows = irows + 1
        totalMFI = totalMFI + cuMTI
        if(irows < totalrows):
            curDate = SourceData.loc[irows,'date']
        else:
            break
    return totalMFI

#计算两个交易日之间的红、绿柱子面积,其中根据输入参数的‘上’、‘下’确定计算红柱子或绿柱子面积
def trdBar (SourceData = 'Trd_Data',startDate = '',endDate = '',direc ='上'):
    totalrows = len(SourceData.index)
    irows = 0
    curDate = (SourceData.loc[irows,'date'])
    totalBar = 0
    #此处停止执行时，日期调整至起始时间点
    while (curDate < startDate):
        irows = irows + 1
        curDate = SourceData.loc[irows,'date']
    while (curDate <= endDate):
        curBar = SourceData.loc[irows,'BAR']
        if(direc == '上') and (curBar > 0):
            totalBar = totalBar + curBar
        elif(direc == '下') and (curBar < 0):
            totalBar = totalBar + curBar
        if(irows < totalrows-1):
            irows = irows + 1
            curDate = SourceData.loc[irows,'date']
        else:
            break
    return totalBar

#以中枢产生前的第一笔或产生三买、三卖后的笔为起点，直至产生中枢，值直接写入参数Bi_Data
def BirowPivot(Bi_Data = 'Bi_Data',irows = 0,BiTrend = '无',pivotCounter = 0):
    totalrows = len(Bi_Data.index)
    if (irows + 3 < totalrows):
        B1Dir = Bi_Data.loc[irows,'Direc']
        B1EndPrice =  Bi_Data.loc[irows,'endPrice']
        B2EndPrice =  Bi_Data.loc[irows + 1,'endPrice']
        B3EndPrice =  Bi_Data.loc[irows + 2,'endPrice']
        B4EndPrice =  Bi_Data.loc[irows + 3,'endPrice']
        B1StartPrice = Bi_Data.loc[irows,'startPrice']
        B2StartPrice = Bi_Data.loc[irows + 1,'startPrice']
        B3StartPrice = Bi_Data.loc[irows + 2,'startPrice']
        B4StartPrice = Bi_Data.loc[irows + 3,'startPrice']
        #原来用的1，3笔，再后来用2、4笔可能效果更好，现在加入参数BiTrend，同时参数也是程序的返回值，在三买后，笔趋势向上，
        #在三卖后，笔趋势向下，在未产生之前，用双重限定
        if (BiTrend =='无'):
            if (B2StartPrice > B4StartPrice) and (B2EndPrice > B4EndPrice) and \
                    (B1StartPrice > B3StartPrice) and (B1EndPrice > B3EndPrice):
                BiTrend = '下'
            elif (B2StartPrice < B4StartPrice) and (B2EndPrice < B4EndPrice) and \
                    (B1StartPrice < B3StartPrice) and (B1EndPrice < B3EndPrice) :
                BiTrend = '上'
            else:
               BiTrend = '无'
        #起始笔和的方向和4笔的子趋势方向不一致，则进入下一笔，判断方向一致与否是第1笔
        # 与第三笔比较，如果没有明确方向，将第一笔当成中枢进入笔。
        if (BiTrend != '无')and (B1Dir != BiTrend):
            Bi_Data.loc[irows,'MB'] = '非中枢起始笔'
            irows = irows + 1
            return irows,BiTrend,pivotCounter
        else:
            if(B1Dir == '上'):
                if(B4EndPrice > B2StartPrice):
                    irows = irows + 2
                    Bi_Data.loc[irows,'MB'] = '中枢连接笔'
                    Bi_Data.loc[irows + 1,'MB'] = '中枢连接笔'
                    return irows,BiTrend,pivotCounter
                else:
                    Bi_Data.loc[irows,'MB2'] = '进入中枢段'
                    Bi_Data.loc[irows + 1,'MB'] = '中枢第一笔'
                    Bi_Data.loc[irows + 2,'MB'] = '中枢第二笔'
                    Bi_Data.loc[irows + 3, 'MB'] ='中枢第三笔'
                    pivotCounter = pivotCounter + 1
                    if (B3EndPrice > B1EndPrice):
                        GG = B3EndPrice
                        ZG = B1EndPrice
                    else:
                        ZG = B3EndPrice
                        GG = B1EndPrice
                    if(B2EndPrice < B4EndPrice):
                        DD = B2EndPrice
                        ZD = B4EndPrice
                    else:
                        ZD = B2EndPrice
                        DD = B4EndPrice
                    Bi_Data.loc[irows + 3, 'ZG'] = ZG
                    Bi_Data.loc[irows + 3, 'ZD'] = ZD
                    Bi_Data.loc[irows + 3, 'DD'] = DD
                    Bi_Data.loc[irows + 3, 'GG'] = GG
                    irows = irows + 4
            elif(B1Dir == '下'):
                 if(B4EndPrice < B2StartPrice):
                     irows = irows + 2
                     Bi_Data.loc[irows,'MB'] = '中枢连接笔'
                     Bi_Data.loc[irows + 1,'MB'] = '中枢连接笔'
                     return irows,BiTrend,pivotCounter
                 else:
                    Bi_Data.loc[irows,'MB2'] = '进入中枢段'
                    Bi_Data.loc[irows + 1,'MB'] = '中枢第一笔'
                    Bi_Data.loc[irows + 2,'MB'] = '中枢第二笔'
                    Bi_Data.loc[irows + 3, 'MB'] ='中枢第三笔'
                    pivotCounter = pivotCounter + 1
                    if (B4EndPrice > B2EndPrice):
                        GG = B4EndPrice
                        ZG = B2EndPrice
                    else:
                        ZG = B4EndPrice
                        GG = B2EndPrice
                    if(B3EndPrice < B1EndPrice):
                        DD = B3EndPrice
                        ZD = B1EndPrice
                    else:
                        ZD = B3EndPrice
                        DD = B1EndPrice
                    Bi_Data.loc[irows + 3, 'ZG'] = ZG
                    Bi_Data.loc[irows + 3, 'ZD'] = ZD
                    Bi_Data.loc[irows + 3, 'DD'] = DD
                    Bi_Data.loc[irows + 3, 'GG'] = GG
                    irows = irows + 4
                #处理中枢震荡
            while (irows < totalrows):
                BiDir = Bi_Data.loc[irows, 'Direc']
                BiEndPrice = Bi_Data.loc[irows, 'endPrice']
                if(BiDir == '上'):
                    if (BiEndPrice > GG):
                        #当下一笔确认回到中枢中，或产生三买时，再修改这一笔的状态
                        Bi_Data.loc[irows,'MB'] = '新高高，待确认'
                        if (Bi_Data.loc[irows - 1,'MB'] == '新低低，待确认'):
                            Bi_Data.loc[irows - 1,'MB'] = '中枢震荡'
                            Bi_Data.loc[irows - 1,'MB4'] = '新低低'
                            DD = Bi_Data.loc[irows - 1, 'endPrice']
                            Bi_Data.loc[irows - 1, 'DD'] = DD
                    elif(ZG < BiEndPrice) and (BiEndPrice < GG):
                        Bi_Data.loc[irows,'MB'] = '中枢震荡'
                        Bi_Data.loc[irows,'MB4'] ='ZG和GG之间'
                        if (Bi_Data.loc[irows - 1,'MB'] == '新低低，待确认'):
                            Bi_Data.loc[irows - 1,'MB'] = '中枢震荡'
                            Bi_Data.loc[irows - 1,'MB4'] = '新低低'
                            DD = Bi_Data.loc[irows - 1, 'endPrice']
                            Bi_Data.loc[irows - 1, 'DD'] = DD
                    elif(ZD < BiEndPrice) and (BiEndPrice < ZG):
                        Bi_Data.loc[irows,'MB'] = '中枢震荡'
                        Bi_Data.loc[irows,'MB4'] ='ZD和ZG之间'
                        if (Bi_Data.loc[irows - 1,'MB'] == '新低低，待确认'):
                            Bi_Data.loc[irows - 1,'MB'] = '中枢震荡'
                            Bi_Data.loc[irows - 1,'MB4'] = '新低低'
                            DD = Bi_Data.loc[irows - 1, 'endPrice']
                            Bi_Data.loc[irows - 1, 'DD'] = DD
                    elif(BiEndPrice < ZD):
                        Bi_Data.loc[irows,'MB'] = '形成三卖'
                        Bi_Data.loc[irows,'BSP'] = '三卖'
                        Bi_Data.loc[irows -1,'MB3'] = '离开中枢段'
                        BiTrend = '下'
                        return (irows -1),BiTrend,pivotCounter
                elif(BiDir == '下'):
                    if (BiEndPrice < DD):
                        #当下一笔确认回到中枢中，或产生三买时，再修改这一笔的状态
                        Bi_Data.loc[irows,'MB'] = '新低低，待确认'
                        if(Bi_Data.loc[irows - 1,'MB'] == '新高高，待确认'):
                            Bi_Data.loc[irows - 1,'MB'] = '中枢震荡'
                            Bi_Data.loc[irows - 1,'MB4'] = '新高高'
                            GG = Bi_Data.loc[irows - 1, 'endPrice']
                            Bi_Data.loc[irows - 1, 'GG'] = GG
                    elif(DD < BiEndPrice) and (BiEndPrice < ZD):
                        Bi_Data.loc[irows,'MB'] = '中枢震荡'
                        Bi_Data.loc[irows,'MB4'] = 'DD和ZD之间'
                        if(Bi_Data.loc[irows - 1,'MB'] == '新高高，待确认'):
                            Bi_Data.loc[irows - 1,'MB'] = '中枢震荡'
                            Bi_Data.loc[irows - 1,'MB4'] = '新高高'
                            GG = Bi_Data.loc[irows - 1, 'endPrice']
                            Bi_Data.loc[irows - 1, 'GG'] = GG
                    elif(ZD < BiEndPrice) and (BiEndPrice < ZG):
                        Bi_Data.loc[irows,'MB'] = '中枢震荡'
                        Bi_Data.loc[irows,'MB4'] = 'ZD和ZG之间'
                        if(Bi_Data.loc[irows - 1,'MB'] == '新高高，待确认'):
                            Bi_Data.loc[irows - 1,'MB'] = '中枢震荡'
                            Bi_Data.loc[irows - 1,'MB4'] = '新高高'
                            GG = Bi_Data.loc[irows - 1, 'endPrice']
                            Bi_Data.loc[irows - 1, 'GG'] = GG
                    elif(BiEndPrice > ZG):
                        Bi_Data.loc[irows,'MB'] = '形成三买'
                        Bi_Data.loc[irows,'BSP'] = '三买'
                        Bi_Data.loc[irows -1,'MB3'] = '离开中枢段'
                        BiTrend = '上'
                        return (irows -1),BiTrend,pivotCounter
                irows = irows + 1
    elif totalrows <= 3:
        Bi_Data.loc[irows,'MB'] = '不足三笔，不形成新中枢'
        irows = totalrows
        return irows,BiTrend,pivotCounter
    else:
        Bi_Data.loc[irows,'MB'] = '不足三笔，不形成新中枢'
        irows = totalrows
        return irows,BiTrend,pivotCounter
    return irows,BiTrend,pivotCounter
    #对中枢延续进行处理，

def BiNoLidu(Pivot_Data = 'Pivot_Data'):
    Pivot_Data['ZSBiNo'] = None
    Pivot_Data['ZSLidu'] = None
    totalrows = len(Pivot_Data.index)
    irows = 0
    inrows = []
    outrows = []
    while (irows < totalrows):
        if (Pivot_Data.loc[irows,'MB2'] =='进入中枢段'):
            inrows.append(irows)
        if (Pivot_Data.loc[irows,'MB3'] =='离开中枢段'):
            outrows.append(irows)
        irows = irows + 1
    ComZSNo = len(outrows) #已完成中枢数
    irows = 0
    zsindex = 0
    while(zsindex < ComZSNo):
        inIndex = inrows[zsindex]
        outIndex = outrows[zsindex]
        Pivot_Data.loc[outIndex,'ZSBiNo'] = outIndex - inIndex
        Pivot_Data.loc[inIndex,'ZSBiNo'] = 0
        #移动到中枢进入段
        irows = inIndex
        inXL = Pivot_Data.loc[inIndex,'XL']
        irows = irows + 1
        inDir = Pivot_Data.loc[inIndex,'Direc']
        while(inIndex < irows <= outIndex):
            curXL =  Pivot_Data.loc[irows,'XL']
            curDir = Pivot_Data.loc[irows,'Direc']
            BiCounter = irows -inIndex
            Pivot_Data.loc[irows,'ZSBiNo'] = BiCounter
            MB = Pivot_Data.loc[irows,'MB']
#            print(Pivot_Data)
            MB4 = Pivot_Data.loc[irows,'MB4']
            if(curDir == inDir):
                if abs(curXL) > abs(inXL):
                    Pivot_Data.loc[irows,'ZSLidu'] = '强'
                elif abs(curXL) < abs(inXL):
                    Pivot_Data.loc[irows,'ZSLidu'] = '弱'
                    if(irows - inIndex > 3) and (curDir =='上'):
                        if(MB == '新高高，待确认') or (MB4 =='新高高'):
                            Pivot_Data.loc[irows,'BSP'] = '一卖'
                            nxtBSpoint = Pivot_Data.loc[irows + 2,'BSP']
                            nxtKSLi = Pivot_Data.loc[irows + 2,'Lidu']  #'开山力度'
                            nxtKSGd = Pivot_Data.loc[irows + 2,'HiLow']
                            if(nxtKSLi == '弱') or (nxtKSGd == '低'):
                                Pivot_Data.loc[irows + 2,'BSP'] = '二卖'
                    elif(curDir =='下'):
                        if(MB == '新低低，待确认') or (MB4 =='新低低'):
                             Pivot_Data.loc[irows,'BSP'] = '一买'
                             nxtBSPoint = Pivot_Data.loc[irows + 2,'BSP']
                             nxtKSLi = Pivot_Data.loc[irows + 2,'Lidu']  #'开山力度'
                             nxtKSGd = Pivot_Data.loc[irows + 2,'HiLow']
                             if(nxtKSLi == '弱') or (nxtKSGd == '高'):
                                if(nxtBSPoint !='三买'):
                                    Pivot_Data.loc[irows + 2,'BSP'] = '二买'
                                else:
                                    Pivot_Data.loc[irows + 2,'BSP'] = '二三买合一'
            else:
                Pivot_Data.loc[irows,'ZSLidu'] = '无'
            irows = irows + 1
        zsindex = zsindex + 1
    #处理取后一个未完成中枢的内部力度情况
    if(len(inrows) > len(outrows)):
        inIndex = inrows[zsindex]
        inXL = Pivot_Data.loc[inIndex,'XL']
        inDir = Pivot_Data.loc[inIndex,'Direc']
        while(irows < totalrows):
            curXL =  Pivot_Data.loc[irows,'XL']
            curDir = Pivot_Data.loc[irows,'Direc']
            if(curDir == inDir):
                if abs(curXL) > abs(inXL):
                    Pivot_Data.loc[irows,'ZSLidu'] = '强'
                elif abs(curXL) < abs(inXL):
                    Pivot_Data.loc[irows,'ZSLidu'] = '弱'
                    MB = Pivot_Data.loc[irows,'MB']
                    MB4 = Pivot_Data.loc[irows,'MB4']
            else:
                Pivot_Data.loc[irows,'ZSLidu'] = '无'
            irows = irows + 1
    return  Pivot_Data

#对于输入的笔，计算其中枢内容
def BiPivot (Bi_Data = 'Bi_Data',BiTrend = '无'):
    Pivot_Data = DataFrame(Bi_Data.values,columns= Bi_Data.columns)
    Bi_Data['ZD'] = '无'
    Bi_Data['ZG'] = '无'
    Bi_Data['DD'] = '无'
    Bi_Data['GG'] = '无'
    Bi_Data['BSP'] = '无' #买卖点
    Bi_Data['MB'] = '无'
    Bi_Data['MB2'] = '无'
    Bi_Data['MB3'] = '无'
    Bi_Data['MB4'] = '无'
    totalrows = len(Bi_Data)
    irows = 0
    #找第一个成立的中枢,原来的程序中，由于线段方向确定，用第一笔方向代表区域方向，这里改为用第1笔和第4笔的结束点比较确定短线趋势。
    #如第一笔方向与短线趋势相同，则判断是否有中枢，如果不相同，就从下一笔为起点判断（irows = irows + 1）
    pivotCounter = 0
    while (irows < totalrows):
        irows,BiTrend,pivotCounter = BirowPivot(Bi_Data,irows,BiTrend,pivotCounter)
    Pivot_Data = ReIndex(Bi_Data)
    if(pivotCounter > 1): #如果有一个以上中枢，如果是第一个中枢还没有形成，不宜比较中枢力度，不执行程序
        Pivot_Data = BiNoLidu(Pivot_Data)
    return Pivot_Data

#输入处理后的中枢数据，返回最近中枢有无，以及中枢边界（ZD,ZG,DD,GG）
def ZhongShu(Pivot_Data='Pivot_Data'):
    ZD = Last_Value_inCol(Pivot_Data,'ZD')
    ZG = Last_Value_inCol(Pivot_Data,'ZG')
    DD = Last_Value_inCol(Pivot_Data,'DD')
    GG = Last_Value_inCol(Pivot_Data,'GG')
    totalrows = len(Pivot_Data)
    Dir = Pivot_Data.loc[totalrows-1,'Direc']
#    ZSBiNo = Last_Value_inCol(Pivot_Data,'ZSBiNo')
    zs_data = Series([ZD,ZG,DD,GG,Dir],index=['ZD','ZG','DD','GG','Direc'])
    if(ZD=='无'):
        ZSExist = False
    else:
        ZSExist = True
    return ZSExist,zs_data


# 判断三买是否存在的函数，存在返回Ture,不存在返回False
def BirowThirdBuy(Bi_Data = 'Bi_Data',irows = 0,BiTrend = '下',pivotCounter = 0):
    totalrows = len(Bi_Data.index)
    if (irows + 3 < totalrows):
        B1Dir = Bi_Data.loc[irows,'Direc']
        B1EndPrice =  Bi_Data.loc[irows,'endPrice']
        B2EndPrice =  Bi_Data.loc[irows + 1,'endPrice']
        B3EndPrice =  Bi_Data.loc[irows + 2,'endPrice']
        B4EndPrice =  Bi_Data.loc[irows + 3,'endPrice']
        B1StartPrice = Bi_Data.loc[irows,'startPrice']
        B2StartPrice = Bi_Data.loc[irows + 1,'startPrice']
        B3StartPrice = Bi_Data.loc[irows + 2,'startPrice']
        B4StartPrice = Bi_Data.loc[irows + 3,'startPrice']
        #原来用的1，3笔，再后来用2、4笔可能效果更好，现在加入参数BiTrend，同时参数也是程序的返回值，在三买后，笔趋势向上，
        #在三卖后，笔趋势向下，在未产生之前，用双重限定
        if (BiTrend =='无'):
            if (B2StartPrice > B4StartPrice) and (B2EndPrice > B4EndPrice) and \
                    (B1StartPrice > B3StartPrice) and (B1EndPrice > B3EndPrice):
                BiTrend = '下'
            elif (B2StartPrice < B4StartPrice) and (B2EndPrice < B4EndPrice) and \
                    (B1StartPrice < B3StartPrice) and (B1EndPrice < B3EndPrice) :
                BiTrend = '上'
            else:
               BiTrend = '无'
        #起始笔和的方向和4笔的子趋势方向不一致，则进入下一笔，判断方向一致与否是第1笔
        # 与第三笔比较，如果没有明确方向，将第一笔当成中枢进入笔。
        if (BiTrend != '无')and (B1Dir != BiTrend):
            irows = irows + 1
            return irows,BiTrend,pivotCounter,False
        else:
            if(B1Dir == '上'):
                if(B4EndPrice > B2StartPrice):
                    irows = irows + 2
                    return irows,BiTrend,pivotCounter, False
                else:
                    pivotCounter = pivotCounter + 1
                    if (B3EndPrice > B1EndPrice):
                        GG = B3EndPrice
                        ZG = B1EndPrice
                    else:
                        ZG = B3EndPrice
                        GG = B1EndPrice
                    if(B2EndPrice < B4EndPrice):
                        DD = B2EndPrice
                        ZD = B4EndPrice
                    else:
                        ZD = B2EndPrice
                        DD = B4EndPrice
                    Bi_Data.loc[irows + 3, 'ZG'] = ZG
                    Bi_Data.loc[irows + 3, 'ZD'] = ZD
                    Bi_Data.loc[irows + 3, 'DD'] = DD
                    Bi_Data.loc[irows + 3, 'GG'] = GG
                    irows = irows + 4
            elif(B1Dir == '下'):
                 if(B4EndPrice < B2StartPrice):
                     irows = irows + 2
                     return irows,BiTrend,pivotCounter,False
                 else:
                    pivotCounter = pivotCounter + 1
                    if (B4EndPrice > B2EndPrice):
                        GG = B4EndPrice
                        ZG = B2EndPrice
                    else:
                        ZG = B4EndPrice
                        GG = B2EndPrice
                    if(B3EndPrice < B1EndPrice):
                        DD = B3EndPrice
                        ZD = B1EndPrice
                    else:
                        ZD = B3EndPrice
                        DD = B1EndPrice
                    Bi_Data.loc[irows + 3, 'ZG'] = ZG
                    Bi_Data.loc[irows + 3, 'ZD'] = ZD
                    Bi_Data.loc[irows + 3, 'DD'] = DD
                    Bi_Data.loc[irows + 3, 'GG'] = GG
                    irows = irows + 4
                #处理中枢震荡
            while (irows < totalrows):
                BiDir = Bi_Data.loc[irows, 'Direc']
                BiEndPrice = Bi_Data.loc[irows, 'endPrice']
                if(BiDir == '上'):
                    if (BiEndPrice > GG):
                        #当下一笔确认回到中枢中，或产生三买时，再修改这一笔的状态
                        Bi_Data.loc[irows,'MB'] = '新高高，待确认'
                        if (Bi_Data.loc[irows - 1,'MB'] == '新低低，待确认'):
                            Bi_Data.loc[irows - 1,'MB'] = '中枢震荡'
                            Bi_Data.loc[irows - 1,'MB4'] = '新低低'
                            DD = Bi_Data.loc[irows - 1, 'endPrice']
                            Bi_Data.loc[irows - 1, 'DD'] = DD
                    elif(ZG < BiEndPrice) and (BiEndPrice < GG):
                        Bi_Data.loc[irows,'MB'] = '中枢震荡'
                        Bi_Data.loc[irows,'MB4'] ='ZG和GG之间'
                        if (Bi_Data.loc[irows - 1,'MB'] == '新低低，待确认'):
                            Bi_Data.loc[irows - 1,'MB'] = '中枢震荡'
                            Bi_Data.loc[irows - 1,'MB4'] = '新低低'
                            DD = Bi_Data.loc[irows - 1, 'endPrice']
                            Bi_Data.loc[irows - 1, 'DD'] = DD
                    elif(ZD < BiEndPrice) and (BiEndPrice < ZG):
                        Bi_Data.loc[irows,'MB'] = '中枢震荡'
                        Bi_Data.loc[irows,'MB4'] ='ZD和ZG之间'
                        if (Bi_Data.loc[irows - 1,'MB'] == '新低低，待确认'):
                            Bi_Data.loc[irows - 1,'MB'] = '中枢震荡'
                            Bi_Data.loc[irows - 1,'MB4'] = '新低低'
                            DD = Bi_Data.loc[irows - 1, 'endPrice']
                            Bi_Data.loc[irows - 1, 'DD'] = DD
                    elif(BiEndPrice < ZD):
                        Bi_Data.loc[irows,'MB'] = '形成三卖'
                        Bi_Data.loc[irows,'BSP'] = '三卖'
                        Bi_Data.loc[irows -1,'MB3'] = '离开中枢段'
                        BiTrend = '下'
                        return (irows -1),BiTrend,pivotCounter,False
                elif(BiDir == '下'):
                    if (BiEndPrice < DD):
                        #当下一笔确认回到中枢中，或产生三买时，再修改这一笔的状态
                        Bi_Data.loc[irows,'MB'] = '新低低，待确认'
                        if(Bi_Data.loc[irows - 1,'MB'] == '新高高，待确认'):
                            Bi_Data.loc[irows - 1,'MB'] = '中枢震荡'
                            Bi_Data.loc[irows - 1,'MB4'] = '新高高'
                            GG = Bi_Data.loc[irows - 1, 'endPrice']
                            Bi_Data.loc[irows - 1, 'GG'] = GG
                    elif(DD < BiEndPrice) and (BiEndPrice < ZD):
                        Bi_Data.loc[irows,'MB'] = '中枢震荡'
                        Bi_Data.loc[irows,'MB4'] = 'DD和ZD之间'
                        if(Bi_Data.loc[irows - 1,'MB'] == '新高高，待确认'):
                            Bi_Data.loc[irows - 1,'MB'] = '中枢震荡'
                            Bi_Data.loc[irows - 1,'MB4'] = '新高高'
                            GG = Bi_Data.loc[irows - 1, 'endPrice']
                            Bi_Data.loc[irows - 1, 'GG'] = GG
                    elif(ZD < BiEndPrice) and (BiEndPrice < ZG):
                        Bi_Data.loc[irows,'MB'] = '中枢震荡'
                        Bi_Data.loc[irows,'MB4'] = 'ZD和ZG之间'
                        if(Bi_Data.loc[irows - 1,'MB'] == '新高高，待确认'):
                            Bi_Data.loc[irows - 1,'MB'] = '中枢震荡'
                            Bi_Data.loc[irows - 1,'MB4'] = '新高高'
                            GG = Bi_Data.loc[irows - 1, 'endPrice']
                            Bi_Data.loc[irows - 1, 'GG'] = GG
                    elif(BiEndPrice > ZG):
                        Bi_Data.loc[irows,'MB'] = '形成三买'
                        Bi_Data.loc[irows,'BSP'] = '三买'
                        Bi_Data.loc[irows -1,'MB3'] = '离开中枢段'
                        BiTrend = '上'
                        return (irows -1),BiTrend,pivotCounter, True
                irows = irows + 1
    elif totalrows <= 3:
        Bi_Data.loc[irows,'MB'] = '不足三笔，不形成新中枢'
        irows = totalrows
        return irows,BiTrend,pivotCounter,False
    else:
        Bi_Data.loc[irows,'MB'] = '不足三笔，不形成新中枢'
        irows = totalrows
        return irows,BiTrend,pivotCounter,False
    return irows,BiTrend,pivotCounter,False

def BiThirdBuy (Bi_Data = 'Bi_Data',BiTrend = '下'):
    Pivot_Data = DataFrame(Bi_Data.values,columns= Bi_Data.columns)
    Pivot_Data['ZD'] = None
    Pivot_Data['ZG'] = None
    Pivot_Data['DD'] = None
    Pivot_Data['GG'] = None
    Pivot_Data['BSP'] = None  #买卖点
    totalrows = len(Bi_Data.index)
    pivotCounter = 0
    ThirdBuyExist = False
    irows = 0
    while (irows < totalrows):
        irows,BiTrend,pivotCounter,ThirdBuyExist = BirowThirdBuy(Bi_Data,irows,BiTrend,pivotCounter )
        if (pivotCounter == 0):
            break
        elif (ThirdBuyExist):
            break
    return ThirdBuyExist

#MACD指标处理，用于补充力度计算的不足
def Data_MACD_BAR(Trd_Data = 'Trd_Data'):
    Trd_Data['EMA12'] = None
    Trd_Data['EMA26'] = None
    Trd_Data['DIF'] = None
    Trd_Data['DEA'] = None
    Trd_Data['BAR'] = None
    totalrows = len(Trd_Data)
    irows = 0
    Trd_Data.loc[irows,'EMA12'] = 0
    Trd_Data.loc[irows,'EMA26'] = 0
    Trd_Data.loc[irows,'DIF'] = 0
    Trd_Data.loc[irows,'DEA'] = 0
    Trd_Data.loc[irows,'BAR'] = 0
    irows = irows + 1
    while (irows < totalrows):
        preEMA12 = Trd_Data.loc[irows-1,'EMA12']
        preEMA26 = Trd_Data.loc[irows-1,'EMA26']
        curClose = Trd_Data.loc[irows,'close']
        Trd_Data.loc[irows,'EMA12'] = preEMA12*11/13 +curClose*2/13
        Trd_Data.loc[irows,'EMA26'] = preEMA26*25/27 +curClose*2/27
        curEMA12 = Trd_Data.loc[irows,'EMA12']
        curEMA26 = Trd_Data.loc[irows,'EMA26']
        Trd_Data.loc[irows,'DIF'] = curEMA12 -curEMA26
        preDEA = Trd_Data.loc[irows-1,'DEA']
        curDIF =  Trd_Data.loc[irows,'DIF']
        Trd_Data.loc[irows,'DEA'] = preDEA * 0.8 + curDIF * 0.2
        curDEA = Trd_Data.loc[irows,'DEA']
        Trd_Data.loc[irows,'BAR'] = curDIF - curDEA
        irows = irows + 1
    return Trd_Data

#计算分析周期每个条形的MFI
def Data_MFI(Trd_Data = 'Trd_Data'):
    Trd_Data['updown'] = None
    Trd_Data['MFI'] = None
    Trd_Data['MFITrend'] = None
    Trd_Data['MFIStatus'] = None
    totalrows = len(Trd_Data)
    irows = 0
    Trd_Data.loc[irows,'updown'] = 0
    Trd_Data.loc[irows,'tickTrend'] = 0
    curPriceHigh = Trd_Data.loc[irows,'high']
    curPriceLow = Trd_Data.loc[irows,'low']
    curtick = Trd_Data.loc[irows,'volume']
    Trd_Data.loc[irows,'MFI'] =(curPriceHigh-curPriceLow)*10000/curtick
    Trd_Data.loc[irows,'MFITrend'] = 0
    irows = irows + 1
    while (irows < totalrows):
        #计算MFI和MFITrend
        curPriceHigh = Trd_Data.loc[irows,'high']
        curPriceLow = Trd_Data.loc[irows,'low']
        curtick = Trd_Data.loc[irows,'volume']
        prePriceHigh = Trd_Data.loc[irows-1,'high']
        prePriceLow = Trd_Data.loc[irows-1,'low']
        pretick = Trd_Data.loc[irows-1,'volume']
        preMFI = Trd_Data.loc[irows-1,'MFI']
        curMFI = (curPriceHigh-curPriceLow)*100000/curtick
        Trd_Data.loc[irows,'MFI'] = curMFI
        if(curtick > pretick):
            Trd_Data.loc[irows,'tickTrend'] = '+'
            curTickTrend = '+'
        elif(curtick < pretick):
            Trd_Data.loc[irows,'tickTrend'] = '-'
            curTickTrend = '-'
        if(curMFI > preMFI):
            Trd_Data.loc[irows,'MFITrend'] = '+'
            curMFITrend = '+'
        elif(curMFI < preMFI):
            Trd_Data.loc[irows,'MFITrend'] = '-'
            curMFITrend = '-'
        if(curTickTrend =='+') and (curMFITrend =='+'):
            Trd_Data.loc[irows,'MFIStatus'] ='绿灯'
        elif(curTickTrend =='-') and (curMFITrend =='-'):
            Trd_Data.loc[irows,'MFIStatus'] ='衰退'
        elif(curTickTrend =='-') and (curMFITrend =='+'):
            Trd_Data.loc[irows,'MFIStatus'] ='伪装'
        elif(curTickTrend =='+') and (curMFITrend =='-'):
            Trd_Data.loc[irows,'MFIStatus'] ='蛰伏'
        #计算涨跌幅
        preClose = Trd_Data.loc[irows-1,'close']
        curClose = Trd_Data.loc[irows,'close']
        Trd_Data.loc[irows,'updown'] = curClose/preClose-1
        irows = irows + 1
    return Trd_Data

#计算给定股票的波动率，
def Stock_Vol(StockCode = 'StockCode',AndCycle = 'D',startDate='startDate',endDate = 'endDate'):
    Trd_Data = Get_TrData_FromTs (StockCode = StockCode,AnaCycle = AndCycle,startDate = startDate,endDate = endDate)
    totalrows = len(Trd_Data)
    irows = 0
    Trd_Data['RiseDown'] = None
    Trd_Data.loc[irows,'RiseDown'] = 0
    irows = irows + 1
    totalRiseDown = 0
    while(irows < totalrows):
        preClose = Trd_Data.loc[irows-1,'close']
        curClose = Trd_Data.loc[irows,'close']
        curRiseDown = curClose/preClose -1
        Trd_Data.loc[irows,'RiseDown'] = curRiseDown
        totalRiseDown = totalRiseDown + curRiseDown
        irows = irows +1
    Mean = totalRiseDown/(totalrows-1)
    irows = 1
    totalDevia = 0
    while(irows < totalrows):
        curRiseDown = Trd_Data.loc[irows,'RiseDown']
        totalDevia = totalDevia + (curRiseDown-Mean)**2
        irows = irows +1
    StockVaria = totalDevia/(totalrows-1)
    return StockVaria

#对于输入的任意股票代码，返回经过处理的笔数据
def Bee_Data(stockcdoe='stockcode',AnaCycle = 'AnaCycle',startDate=None,endDate = None):
    S_Trd_Data = Get_TrData_FromTs (stockcdoe, AnaCycle,startDate,endDate)
    Inclu_Data = Include(S_Trd_Data)
    IniFX_Data = AllFX(Inclu_Data)
    RealFX_Data = TopBottomDistin(IniFX_Data)
    Bi_Data,BiCounter = Bee(RealFX_Data)
    Bi_Data = Bee_Update(Bi_Data,Inclu_Data)
    Bi_Data = Bee_TLidu(Bi_Data,S_Trd_Data)
    Bi_Data = Bee_LLidu(Bi_Data,S_Trd_Data)
#        Bi_Data = Bee_BarLidu(Bi_Data,S_Trd_Data)
#        Bi_Data = Bee_MFILidu(Bi_Data,S_Trd_Data)
    return Bi_Data,BiCounter

#将沪深300中近期交易日不足规定日期特定比例（如90%）的股票从列表中删除，形成新的列表，从而避免程序的运行失败，属于比较低层次的处理方法
def Elimi_No_Trade(FilePath='FilePath',toldays = 'toldays',threshhold = 0.8,AnaCycle = 'D'):
    startDate = get_Trday_of_day(toldays,AnaCycle)
    endDate = get_Trday_of_day(0,AnaCycle)
    stock_code_list = get_hs300stock()
    totalrows = len(stock_code_list)
    irows = 0
    stock_code_list2 = DataFrame([],columns=['stockcode','名称'])
    FilePath2 = 'D:\Chan Data\Source\沪深300成份股有交易'+ AnaCycle + '.xlsx'
    while(irows < totalrows):
        stockcode = stock_code_list.loc[irows,'stockcode']
        print(stockcode)
        stockcode = codeType(stockcode)
        trd_per = trd_day_per(stockcode,AnaCycle,startDate,endDate,toldays)
        if(trd_per >= threshhold):
            BiData,BiNo = Bee_Data(stockcode,AnaCycle,startDate,endDate)
            if(BiNo>6):
                stock_code_list2 = stock_code_list2.append(stock_code_list.iloc[irows].T)
        irows = irows + 1
    stock_code_list2 = ReIndex(stock_code_list2)
    Write_DF_T0_Excel(FilePath2,stock_code_list2,'权重排序')

#将沪深300中近toldays中交易不足80%，或笔数不足五笔的股票从下载列表中去除，并下载数据于指定文件夹的日期目录
def Elimi_No_Trade_Down(FilePath='FilePath',toldays = 'toldays',threshhold = 0.8,AnaCycle = 'D',n=0):
    startDate = get_Trday_of_day(n+toldays,AnaCycle)
    endDate = get_Trday_of_day(n,AnaCycle)
    stock_code_list = get_hs300stock()
    totalrows = len(stock_code_list)
    irows = 0
    stock_code_list2 = DataFrame([],columns=['stockcode','名称'])
    DataName = str(endDate)
    FilePath = FilePath + '\\'+ DataName[0:10]
    mkdir(FilePath)
    FilePath2 = FilePath+ '\\' + '沪深300成份股有交易'+ AnaCycle + '.xls'
    while(irows < totalrows):
        stockcode = stock_code_list.loc[irows,'stockcode']
        print(stockcode)
        stockcode = codeType(stockcode)
        stockname = stock_code_list.loc[irows,'名称']
        trd_per = trd_day_per(stockcode,AnaCycle,startDate,endDate,toldays)
        sheetName1 = 'OriData'
        sheetName2 = AnaCycle+'Bi'
        if(trd_per >= threshhold):
            S_Trd_Data = Get_TrData_FromTs(stockcode,AnaCycle,startDate,endDate)
            Inclu_Data = Include(S_Trd_Data)
            IniFX_Data = AllFX(Inclu_Data)
            RealFX_Data = TopBottomDistin(IniFX_Data)
            Bi_Data,BiNo = Bee(RealFX_Data)
            Bi_Data = Bee_Update(Bi_Data,Inclu_Data)
            Bi_Data = Bee_TLidu(Bi_Data,S_Trd_Data)
            Bi_Data = Bee_LLidu(Bi_Data,S_Trd_Data)
            if(BiNo>5):
                stock_code_list2 = stock_code_list2.append(stock_code_list.iloc[irows].T)
                FilePath3 = FilePath + '\\'+ stockcode +str(AnaCycle)+'.xls'
                writer = ExcelWriter(FilePath3)
                S_Trd_Data.to_excel(writer,sheetName1)
                Bi_Data.to_excel(writer,sheetName2)
                writer.save()
        irows = irows + 1
    stock_code_list2 = ReIndex(stock_code_list2)
    Write_DF_T0_Excel(FilePath2,stock_code_list2,'权重排序')

#将数据表中的数据组合到一条数据
def Trd_Data_Merge(Trd_Data ='Trd_Data'):
    s = Series([0,0,0,0,0,0],index=['date','open','high','low','close','volume'])
    totalrows = len(Trd_Data)
    s['date'] = Trd_Data.loc[totalrows-1,'date']
    s['open'] =Trd_Data.loc[0,'open']
    s['close'] = Trd_Data.loc[totalrows-1,'close']
    s['high']  = max(Trd_Data['high'])
    s['low'] = min(Trd_Data['low'])
    s['volume'] = sum(Trd_Data['volume'])
    return s


#数据更新程序，用前一天更新当下日期，用于实盘产生结果，日线用5分钟/30分钟更新，30分钟直接插入最新值
def Data_Update_Day(FilePath = 'FilePath',SCycle='D',UpdCycle ='30'):
    startdate = get_Trday_of_day(1,'D')
    enddate = get_Trday_of_day(0,UpdCycle)
    endName = enddate[0:10]
    stock_code_list2 = DataFrame([],columns=['stockcode','名称'])
    SourceFolder = FilePath + '\\'+ startdate
    TargetFolder = FilePath + '\\' + endName
    mkdir(TargetFolder)
    CodePath = SourceFolder + '\\'+'沪深300成份股有交易'+SCycle + '.xls'
    stockcodelist = Get_TrdData_FromExcel( CodePath,'权重排序')
    totalrows = len(stockcodelist)
    irows = 0
    while(irows < totalrows):
        stockcode = stockcodelist.loc[irows,'stockcode']
        stockcode = codeType(stockcode)
        SFilePath = SourceFolder + '\\'+str(stockcode) +SCycle+'.xls'
        sheetName1='OriData'
        sheetName2 =SCycle + 'Bi'
        TrData_Source= Get_TrdData_FromExcel(SFilePath,sheetName1)
        TrData_Upd = Get_TrData_FromTs(stockcode,UpdCycle,startdate,enddate)
        totalrows2 = len(TrData_Upd)
        if(totalrows2>=1):
            s =Trd_Data_Merge(TrData_Upd)
            print(stockcode,s)
        irows = irows + 1



'''
#将数据拷贝到指定文件夹,包括源数据，以及笔数据
def Stock_List_Data_Down(Stock_Code_list = 'Stock_Code_list',FilePath = 'FilePath',AnaCycle='D',
                    startDate='startDate',endDate='endDate'):
    irows = 123
    totalrows = len(Stock_Code_list)
    while(irows < totalrows):
        stockcode = Stock_Code_list.loc[irows,'stockcode']
        stockName = Stock_Code_list.loc[irows,'名称']
        stockcode = codeType(stockcode)
        print(irows,stockcode)
        S_Trd_Data = Get_TrData_FromTs (StockCode = stockcode,AnaCycle = AnaCycle,startDate = startDate,endDate =endDate)
        endDateAbri = endDate[0:10]
        FilePath2 = FilePath+'\\'+endDateAbri+'\\'+stockcode+AnaCycle+ '.xls'
        writer = ExcelWriter(FilePath2)
        #返回笔数据
        Bi_Data,BiCounter = Bee_Data(stockcode,AnaCycle,startDate,endDate)
        BiSheet = AnaCycle + 'Bi'
        S_Trd_Data.to_excel(writer,'OriData')
        Bi_Data.to_excel(writer,BiSheet)
        writer.save()
        irows = irows + 1
    return Bi_Data



#在指定路径的Excel源数据中加入新的表格，存储内容为笔数据
def AddBiSheet(FilePath = 'FilePath',stockcode = 'stockcode',AnaCycle = 'D'):
#    FilePath = 'D:\Chan Data\BiDemo'
    FileName = stockcode +AnaCycle + '.xls'
    FilePath  = FilePath + '\\'+ FileName
    S_Trd_Data = Get_TrdData_FromExcel(FilePath,'OriData')
    Inclu_Data = Include(S_Trd_Data)
    IniFX_Data = AllFX(Inclu_Data)
    RealFX_Data = TopBottomDistin(IniFX_Data)
    Bi_Data,BiCounter = Bee(RealFX_Data)
    Bi_Data = Bee_Update(Bi_Data,Inclu_Data)
    Bi_Data = Bee_TLidu(Bi_Data,S_Trd_Data)
#    Bi_Data = BiPivot(Bi_Data)   #这行是为了把中枢找出来
    sheetname = AnaCycle+'Bi'
    writer = ExcelWriter(FilePath)
    S_Trd_Data.to_excel(writer,'OriData')
    Bi_Data.to_excel(writer,sheetname)
    writer.save()
    return Bi_Data


#在指定路径的Excel源数据中加入新的表格，存储内容为中枢数据
def AddPivotSheet(FilePath = 'FilePath',stockcode = 'stockcode',AnaCycle = 'D'):
#    FilePath = 'D:\Chan Data\BiDemo'
    FileName = stockcode +AnaCycle + '.xls'
    FilePath  = FilePath + '\\'+ FileName
    S_Trd_Data = Get_TrdData_FromExcel(FilePath,'OriData')
    Inclu_Data = Include(S_Trd_Data)
    IniFX_Data = AllFX(Inclu_Data)
    RealFX_Data = TopBottomDistin(IniFX_Data)
    Bi_Data,BiCounter = Bee(RealFX_Data)
    Bi_Data = Bee_Update(Bi_Data,Inclu_Data)
    Bi_Data = Bee_TLidu(Bi_Data,S_Trd_Data)
    Pivot_Data = BiPivot(Bi_Data)   #这行是为了把中枢找出来
    sheetname = AnaCycle+'Bi'
    writer = ExcelWriter(FilePath)
    S_Trd_Data.to_excel(writer,'OriData')
    Pivot_Data.to_excel(writer,sheetname)
    writer.save()
    return Pivot_Data
'''


































































