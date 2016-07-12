 # -*- coding: utf-8 -*-
import pandas as pd
import tushare as ts
from pandas import DataFrame
from pandas import ExcelWriter
import os

#配置数据接口，为一系列数据读取文件，当下为Excel，未来为数据库，目前数据完备，未来考虑数据的清洗功能
#从Excel中读取交易数据，在参数中指定文件路径，以及工作表名称，数据按交易日期升序排列,有pandas,目前还未实施处理空数据等容错功能
#这个专用于处理来自于路透的历史数据，未来可能不用
def Get_TrData_FromExc(FilePath= 'file.xlsx',ColIndex='date',Worksheet = 'sheetname'):
    try:
       Trd_Data = pd.read_excel(io=FilePath,sheetname = Worksheet)
    except Exception as err:
        print (str(err))
    Trd_Data = Trd_Data.sort_values(by = ColIndex,ascending =True )
    new_columns = ['date','open','high','low','close','volume']
    Trd_Data = DataFrame(Trd_Data.values, columns = new_columns)
    Trd_Data.sort_values(by = 'date', ascending = True)
    return Trd_Data

# 用TuShare获得股票数据，股票代码默认为sh，分析周期默认为日线
def Get_TrData_FromTs(StockCode = 'sh',AnaCycle = '30',startDate = None,endDate = None):
    df = ts.get_hist_data(code = StockCode,ktype =AnaCycle,start =startDate,end = endDate)
    totalrows = len(df)
    if(totalrows!=0):
        Trd_Data = df[['high','low','open','close','volume']]
        Trd_Data = DataFrame(Trd_Data.sort_index(axis = 0,ascending=True))
        new_columns = ['date','open','high','low','close','volume']
        Trd_Data = DataFrame(Trd_Data,columns=new_columns)
        s = Trd_Data.index
        irows = 0
        totalrows = len(Trd_Data.index)
        Trd_Data.reset_index(drop = True, inplace= True)
        while (irows <= totalrows -1):
            Trd_Data.loc[irows,'date'] = s[irows]
            irows = irows + 1
    else:
        Trd_Data = DataFrame([],columns = ['date','open','high','low','close','volume'])
    return Trd_Data

#从Excel读取数据
def Get_TrdData_FromExcel(FilePath= 'file.xlsx',Worksheet = 'sheetname'): #用Xlrd获取数据
    try:
       Trd_Data = pd.read_excel(io=FilePath,sheetname = Worksheet)
    except Exception as err:
        print (str(err))
    #Trd_Data = Trd_Data.sort_values(by = ColIndex,ascending =True )
    return Trd_Data

#将数据写入Excel,这是用于我周期联合比较的写入方法
def Write_To_Excel(FilePath = 'D:\Chan Program\SZData.xls',S_Trd_Data = '',Inclu_Data = '',IniFX_Data = '',\
           RealFX_Data = '',Bi_Data = '', Pivot_Data = ''):
    writer = ExcelWriter(FilePath)
    S_Trd_Data.to_excel(writer,'OriData')
    Inclu_Data.to_excel(writer,'Inclu')
    IniFX_Data.to_excel(writer,'IniFX')
    RealFX_Data.to_excel(writer,'RealFX')
    Bi_Data.to_excel(writer,'Bi')
    Pivot_Data.to_excel(writer,'BiPivot')
    writer.save()

#将DataFrame类型数据写入指定路径
def Write_DF_T0_Excel(FilePath = 'D:\Chan Program\SZData.xls',df_Data = '',sheetname =''):
    writer = ExcelWriter(FilePath)
    df_Data.to_excel(writer,sheetname)
    writer.save()

#将列表数据（一级）写入Excel，主要用于数据的后续加工，如业绩跟踪
def Write_STo_Excel (FilePath = 'D:\Chan Program\Seleced Stock\SelStock.xls',S_List='',sheetname = 'StockList'):
     new_columns = ['stockcode']
     Selected_Stock = DataFrame(S_List,columns =new_columns)
     writer = ExcelWriter(FilePath)
     Selected_Stock.to_excel(writer,sheetname)
     writer.save()
     return Selected_Stock

#取得全部股票代码列表
def get_stock_code():
    stock_code_list = []
    for root, dirs, files in os.walk('D:\Chan Data\Source\stock data'):
        if files:
            for f in files:
                f = f[2:]
                if '.csv' in f:
                    stock_code_list.append(f.split('.csv')[0])
    return stock_code_list

def get_all_stock():
#用于从文件夹生成所有股票代码的代码。
#    All_Stocde_Code_list =get_stock_code()
#    FilePath = 'D:\Chan Data\Source\All_Stock_Code.xls'
#    Write_STo_Excel(FilePath ,All_Stocde_Code_list,'AllStock')
    FilePath = 'D:\Chan Data\Source\All_Stock_Code.xls'
    All_Stocde_Code_list = pd.read_excel(io=FilePath,sheetname='AllStock',columns='stockcode')
    return All_Stocde_Code_list

#返回沪深300所有股票代码
def get_hs300stock():
    FilePath = 'D:\Chan Data\Source\沪深300成份股.xlsx'
    hs300stock = pd.read_excel(io=FilePath,sheetname='权重排序')
    return hs300stock

#返回沪深300中近100天交易超过90%交易的股票列表
def get_hs300stockOp(AnaCycle = 'D'):
    FilePath = 'D:\Chan Data\Source\沪深300成份股有交易'+AnaCycle+'.xlsx'
    hs300stock = pd.read_excel(io=FilePath,sheetname='权重排序')
    return hs300stock

#将列表数据存入txt文件或从txt文件读出。
def Write_to_txt(fileName = 'InterData.txt',Li='list'):
    pre=str(Li)
    pre=pre.replace("[","")
    pre=pre.replace("]","")+"\n"
    f=open(fileName,'w')
    f.write(pre)
    f.close()

def Read_from_txt(fileName = 'InterData.txt'):
    f=open(fileName,'r')
    i=f.readline() #读取文件内容
    i=i.replace("\n",'')
    stock_code_list=i.split(',')
    f.close()
    return stock_code_list

#数据转换器，将特定数据源的数据转换成与Tushare通用,再存入指定位置，仅日期含开收高低四个值
def TrData_Trans(SFilePath='SFilePath',TFilePath='TFilePath',sheetName = 'sheetName',dateName='date',
                                openName = 'open',highName ='high',lowName='low', closeName='close'):
    df = pd.read_excel(io=SFilePath,sheetname = sheetName)
    Trd_Data = df[[dateName,openName,highName,lowName,closeName]]
    Trd_Data = DataFrame(Trd_Data.values,columns=['date','open','high','low','close'])
    Write_DF_T0_Excel(TFilePath,Trd_Data,'OriData')

#数据转换器，将特定数据源的数据转换成与Tushare通用,再存入指定位置，含日期开收高低、
def TrData_Trans2(SFilePath='SFilePath',TFilePath='TFilePath',sheetName = 'sheetName',dateName='date',
            openName = 'open',highName ='high',lowName='low', closeName='close',peName='peName',pbName='pbName'):
    df = pd.read_excel(io=SFilePath,sheetname = sheetName)
    Trd_Data = df[[dateName,openName,highName,lowName,closeName,peName,pbName]]
    Trd_Data = DataFrame(Trd_Data.values,columns=['date','open','high','low','close','PE','PB'])
    Write_DF_T0_Excel(TFilePath,Trd_Data,'OriData')










































