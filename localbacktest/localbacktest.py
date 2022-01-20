from datetime import datetime, timedelta
import pandas as pd

from localbacktest.data import get_market_data

__all__ = ['LocalBacktest']

class Context():
    '''Context

    Attributes:
        securities (list): security list, eg: ['000001.SZ','600000.SH']
        start_date (str): '2020-09-01'
        end_date (str): '2020-09-01'
        capital (int):
        benchmark (str): '000300.SH'
        commission (float): 0.0003
    '''
    pass

class Position():
    '''Position

    Attributes:
        code (str): 
        cost_price (float):
        amount (float):
        volume (int):
    '''
    pass

class Capital():
    '''Capital

    Attributes:
        available_fund (float): 
        holding_value (float):
        total_asset (float):
    '''
    def __init__(self, init_capital):
        self.available_fund = init_capital
        self.holding_value = 0.0
        self.total_asset = self.available_fund + self.holding_value

class Trade():
    '''Trade

    Attributes:
        code (str): 
        tradeside (str):
        volume (int):
        price (float):
        amount (float):
        err_msg (str):
    '''
    pass

class LocalBacktest():
    '''Trade

    Attributes:
        __init_func (func): 
            Args:
                context (Context):

        __handle_data_func (func):
            Args:
                datetime (datetime)
                context (Context)
                data (NULL): 因为请求远程数据较慢，所以本地回测暂不主动输送数据，可自行按需请求
    '''

    def __init__(self, init_func, handle_data_func):
        self.__context = Context()
        self.__init_func = init_func
        self.__handle_data_func = handle_data_func

    def run(self):
        self.__init_func(self.__context)
        self.__capital = Capital(self.__context.capital)
        self.__position_dict = {}
        self.__trade_list = []
        start = datetime.strptime(self.__context.start_date, "%Y-%m-%d")
        end = datetime.strptime(self.__context.end_date, "%Y-%m-%d")
        for i in range((end - start).days+1): 
            current_date = start + timedelta(days = i) 
            print(current_date)

    '''order

    Args:
        code (str):
        volume (int):
        trade_side (bool): 'buy' or 'sell'
        price (str): 'close' or 'open'

    Returns:
        bool: success or not
    '''
    def order(self, code, volume, trade_side, price = 'open'):
        pass
            
