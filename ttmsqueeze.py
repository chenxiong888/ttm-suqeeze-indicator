# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 09:42:53 2022

@author: Jerry Chen
"""
import numpy as np
import talib as ta
import pandas as pd
import GetData

def in_squeeze(df):
   return df['lower_band'] > df['lower_keltner'] and df['upper_band'] < df['upper_keltner']

def GetSqueeze(df,N=20):
    close=np.array(df['close'])
    high=np.array(df['high'])
    low=np.array(df['low'])
    #get bulling belt
    
    df['upper_band'], middleband, df['lower_band'] = ta.BBANDS(close, timeperiod=N, nbdevup=2, nbdevdn=2, matype=0)
    #get ATR
    atr=ta.ATR(high, low, close,timeperiod=N)
    #Get keltner 
    ma=ta.MA(close,timeperiod=N)
    df['upper_keltner']=ma+atr*1.5
    df['lower_keltner']=ma-atr*1.5
    #Get Mom
    mom=ta.MOM(close,timeperiod=N)
    #get squeeze status
    df['squeeze_on'] = df.apply(in_squeeze, axis=1)
    str=""
    if df.iloc[-3]['squeeze_on'] and not df.iloc[-1]['squeeze_on']:
        if mom.tolist()[-1]>0:
            str="做多"
        else:
            str="做空"
        return True,str
    else:
        return False,str#return two result,one means if in squeeze status,other is direction
    
if __name__ == "__main__":
    gd=GetData.GetData()
    allstock=gd.GetAllStock()
    result=pd.DataFrame(columns=['代码','方向'])

    j=0

    # , stop)allstock.ts_code  :
    for i in allstock.ts_code:
        
        try:
            j=j+1
            # time.sleep(0.15)
            
            df=gd.GetAStockData(tscode=i,period=250)
            if len(df)>20:
                print(i)
                ret,str=GetSqueeze(df)
                if ret:
                    print(i,str)
                    feature={}
                    feature.update({"代码":i})
                    feature.update({"方向":str})
                    result=result.append(feature,ignore_index=True)
                    
        except OSError:
            pass
        continue  
    print(result)
    result.to_excel("result.xls")