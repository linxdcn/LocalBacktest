import pandas as pd
import numpy as np

wind_init = False
wind_datasource = any

def get_market_data(security, start_date, end_date):
    '''get_market_data

    接入数据源要求：
    * 价格为前复权数据
    * 日期序列为交易日，包括停牌日期
    * 停牌数据用np.nan填充

    Args:
        security (list):
        start_date (str): '2020-09-01'
        end_date (str): '2020-09-01'

    Returns:
        dict:
            key (str): security
            value (DataFrame):
                index (datetime):
                open (float):
                close (float):
                volume (int):
    '''
    print(__get_from_wind(security, start_date, end_date))

def __get_from_wind(security, start_date, end_date):
    global wind_init
    global wind_datasource
    if not wind_init:
        from WindPy import w
        w.start()
        wind_init = True
        wind_datasource = w
    
    result = {}
    for code in security:
        error, data = wind_datasource.wsd(code, "open,close,volume", start_date, end_date, "PriceAdj=F", usedf=True)
        if error == 0:
            data.columns=data.columns.map(lambda x:x.lower())
            data.replace(0.0, np.nan)
            result[code] = data
    return result

get_market_data(["603990.SH"], "2021-12-21", "2022-01-19")
get_market_data(["603990.SH", "600030.SH"], "2021-12-21", "2022-01-19")