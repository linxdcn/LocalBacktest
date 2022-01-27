from datetime import datetime
import pandas as pd
import numpy as np

from localbacktest.data import get_market_data
from localbacktest.plot import basic_plot

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
        security (str): 
        amount (float):
        volume (int):
        last_price (float)
    '''
    def __init__(self, security, amount, volume, last_price):
        self.security = security
        self.amount = amount
        self.volume = volume
        self.last_price = last_price

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
        security (str): 
        tradeside (str):
        volume (int):
        price (float):
        amount (float):
        commission (float):
        status (int): 0 for success, > 0 for error
        err_msg (str):
    '''
    def __init__(self, security, tradeside, volume):
        self.security = security
        self.tradeside = tradeside
        self.volume = volume
        self.price = 0.0
        self.amount = 0.0
        self.commission = 0.0
        self.status = None
        self.err_msg = None

    def as_dict(self):
        return {'security': self.security, 'tradeside': self.tradeside, 'volume': self.volume, 'price': self.price, 'amount': self.amount, 'commission': self.commission, 'status': self.status, 'err_msg': self.err_msg}

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
                data (None): 因为请求远程数据较慢，所以本地回测暂不主动输送数据，可自行按需请求
    '''

    def __init__(self, init_func, handle_data_func):
        self.__context = Context()
        self.__context.commission = 0
        self.__init_func = init_func
        self.__handle_data_func = handle_data_func

    def run(self):
        self.__init_func(self.__context)

        # 回测全过程变量
        self.__capital = Capital(self.__context.capital)
        self.__position_dict = {} #仓位, key为证券代码
        self.__trade_list = [] #交易记录
        self.__account_nav = [] #账户净值
        self.__lastday_asset = self.__capital.total_asset #昨日总资产
        self.__marketdata_df = get_market_data(self.__context.securities, 
                                        self.__context.start_date,
                                        self.__context.end_date,
                                        fields=['open', 'close', 'pre_close']) #回测区间所有行情数据
        benchmark_df = get_market_data([self.__context.benchmark], 
                                        self.__context.start_date,
                                        self.__context.end_date,
                                        fields=['open', 'close', 'pre_close'])
        benchmark_df.reset_index(inplace=True)
        self.__nav = pd.DataFrame(columns=['datetime', 'nav', 'benchmark'])
        self.__nav['benchmark'] = (benchmark_df['close'] / benchmark_df['pre_close']).cumprod()
        self.__nav['datetime'] = benchmark_df['datetime']
        
        trade_days = [d.strftime('%Y-%m-%d') for d in benchmark_df['datetime']]
        for d in trade_days: 
            # 每次回测的临时变量
            self.__current_date = datetime.strptime(d, "%Y-%m-%d")
            self.__data_cache = {}
            self.__handle_data_func(self.__current_date, self.__context, None)

            # 资产更新
            for security, position in self.__position_dict.items():
                date_str = self.__current_date.strftime("%Y-%m-%d")
                row_data = self.__get_row_data(security, date_str)
                increase_profit = (row_data.loc['close'] - position.last_price) * position.volume
                position.amount += increase_profit
                position.last_price = row_data.loc['close']
                self.__capital.holding_value += increase_profit
                self.__capital.total_asset += increase_profit

            # 计算当日净值
            profit_ratio = self.__capital.total_asset / self.__lastday_asset
            self.__lastday_asset = self.__capital.total_asset
            self.__account_nav.append(self.__account_nav[-1] * profit_ratio if len(self.__account_nav) > 0 else profit_ratio)
        
        self.__nav['nav'] = self.__account_nav

    '''order

    Args:
        security (str):
        volume (int):
        trade_side (bool): 'buy' or 'sell'
        price (str): 'close' or 'open', default='close'

    Returns:
        bool: True or False
    '''
    def order(self, security, volume, tradeside, price = 'close'):
        context = self.__context
        capital = self.__capital
        position_dict = self.__position_dict
        date_str = self.__current_date.strftime("%Y-%m-%d")
        trade = Trade(security, tradeside, volume)

        #行情数据处理
        row_data = self.__get_row_data(security, date_str)
        if row_data is None:
            trade.status = 99
            trade.err_msg = '无行情数据'
            return False  

        if np.isnan(row_data.loc[price]):
            trade.status = 99
            trade.err_msg = '停牌禁止交易'
            return False

        target_price = round(row_data.loc[price], 2)
        #买入方向
        if tradeside == 'buy':
            
            buy_capital = round(target_price * volume * (1 + context.commission), 2)
            if buy_capital > capital.available_fund:
                trade.status = 99
                trade.err_msg = '资金不足'
                return False

            trade.status = 0
            trade.price = target_price
            trade.amount = trade.price * trade.volume
            trade.commission = round(target_price * volume * context.commission, 2)

            position = position_dict.get(security, Position(security, 0.0, 0.0, 0))
            increase_profit = (target_price - position.last_price) * position.volume
            position.volume += volume
            position.amount += increase_profit + target_price * volume
            position.last_price = target_price
            position_dict[security] = position

            capital.available_fund -= buy_capital
            capital.holding_value += target_price * volume + increase_profit
            capital.total_asset = capital.available_fund + capital.holding_value

        #卖出方向
        if tradeside == 'sell':
            position = position_dict.get(security, Position(security, 0.0, 0.0, 0))
            if position.volume < volume:
                trade.status = 99
                trade.err_msg = '证券不足'
                return False   
            
            sell_capital = round(target_price * volume * (1 - context.commission), 2)
            trade.status = 0
            trade.price = target_price
            trade.amount = trade.price * trade.volume
            trade.commission = round(target_price * volume * context.commission, 2)

            position.volume -= volume
            increase_profit = (target_price - position.last_price) * position.volume
            position.amount += -target_price * volume + increase_profit
            position.last_price = target_price
            position_dict[security] = position

            capital.available_fund += sell_capital
            capital.holding_value -= target_price * volume
            capital.total_asset = capital.available_fund + capital.holding_value
        
        self.__trade_list.append(trade)
        return True

    def summary_result(self):
        dict = {
                    "returns": self.__nav['nav'].iloc[-1] - 1,
                    "available_fund": self.__capital.available_fund,
                    "holding_value": self.__capital.holding_value
                }
        return pd.DataFrame([dict])

    def summary_nav(self):
        return self.__nav

    def summary_trade(self):
        return pd.DataFrame([t.as_dict() for t in self.__trade_list])

    def plot(self):
        basic_plot(self.__nav)

    def __get_row_data(self, security, date_str):
        try:
            return self.__marketdata_df.loc[security, date_str]
        except KeyError:
            try:
                key = security + date_str
                if key in self.__data_cache:
                    return self.__data_cache[key]
                df = get_market_data([security], date_str, date_str)
                self.__data_cache[key] = df
                return df.loc[security, date_str]
            except KeyError:
                return None 