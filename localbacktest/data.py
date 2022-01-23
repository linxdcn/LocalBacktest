import pandas as pd
import numpy as np
from datetime import datetime

from localbacktest.common import LbtConfig

wind_init = False
wind_datasource = any
jq_init = False

__all__ = ['get_market_data']

def get_market_data(security, start_date, end_date):
    '''get_market_data

    接入数据源要求:
    * 价格为前复权数据
    * 日期序列为交易日，包括停牌日期
    * 停牌数据用np.nan填充

    Args:
        security (list): 后缀说明: 上交所,SH; 深交所,SZ; 北交所,BJ
        start_date (str): '2020-09-01'
        end_date (str): '2020-09-01'

    Returns:
        DataFrame: a multiIndex Daframe, a simple example:
                                     open  close       volume
            security    datetime                             
            000001.SH   2021-12-21  17.49  17.59   89373404.0
                        2021-12-22  17.62  17.39   97692775.0
                        2021-12-23  17.40  17.32  105957594.0
            000002.SH   2021-12-21  19.49  20.31  159263253.0
                        2021-12-22  20.29  19.86   96198591.0
                        2021-12-23  19.87  19.65   69722678.0
    '''
    if LbtConfig.get_datasource() == 'wind':
        return __get_from_wind(security, start_date, end_date)
    elif LbtConfig.get_datasource() == 'jq':
        return __get_from_joinquant(security, start_date, end_date)
    else:
        return None

def __get_from_wind(security, start_date, end_date):
    global wind_init
    global wind_datasource
    if not wind_init:
        from WindPy import w
        w.start()
        wind_init = True
        wind_datasource = w
    
    if (len(security) == 1):
        error, result = wind_datasource.wsd(security, 'open,close,volume', start_date, end_date, "PriceAdj=F", usedf=True)
        result.columns = [s.lower() for s in result.columns]
        result.replace(0, np.nan, inplace=True)
        result['security'] = security[0]
        result['datetime'] = result.index
        result.set_index(['security', 'datetime'], inplace=True)
        return result
    else:
        result = pd.DataFrame(columns=['datetime', 'security', 'open', 'close', 'volume'])
        for col in ['open', 'close', 'volume']:
            error, data = wind_datasource.wsd(security, col, start_date, end_date, "PriceAdj=F;Fill=Blank", usedf=True)
            idx = 0
            row = len(data)
            for s in data.columns:
                for i in range(row):
                    if col == 'open':
                        result.loc[idx, 'datetime'] = data.index[i]
                        result.loc[idx, 'security'] = s
                    result.loc[idx, col] = data[s].iloc[i]
                    idx += 1
        result.set_index(['security', 'datetime'], inplace=True)
        result.replace(0, np.nan, inplace=True)
        return result

    

def __get_from_joinquant(security, start_date, end_date):
    global jq_init
    from jqdatasdk import auth, get_price
    if not jq_init:
        auth(LbtConfig.get_jq_user(), LbtConfig.get_jq_password())
        jq_init = True
    to_jqcode = lambda s : s.replace('SH', 'XSHG').replace('SZ', 'XSHE')
    from_fqcode = lambda s : s.replace('XSHG', 'SH').replace('XSHE', 'SZ')
    new_security = [to_jqcode(s) for s in security]
    result = get_price(new_security, start_date, end_date, fields=['open', 'close', 'volume'], panel=False, fill_paused=False)
    result.rename(columns={"time": "datetime", "code": "security"}, inplace=True)
    result['security'] = result['security'].apply(from_fqcode)
    result.set_index(['security', 'datetime'], inplace=True)
    result.replace(0, np.nan, inplace=True)
    return result