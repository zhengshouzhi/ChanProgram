# -*- coding: utf-8 -*-
from DataInter import *
import pandas as pd
#应用1，找到最近的中枢，输入笔数据,找到最近的中枢。
def Nearest_ZS(Bi_Data = 'Bi_Data'):
    print('come on')

if __name__=="__main__":
    File_day = '600501LVD'
    File_thir = '600501LV30'
    FilePath = FilePath = 'D:\Chan Data\Data'+'\\'+ File_day+  '.xls'
    Bi_Data = pd.read_excel(io=FilePath,sheetname = 'Bi')
    print(Bi_Data)