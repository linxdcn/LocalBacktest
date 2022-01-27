from localbacktest import *

def initialize(context):
    context.securities = ['600030.SH']
    context.start_date = '2021-08-01'
    context.end_date = '2021-09-01'
    context.capital = 50000
    context.benchmark = '000300.SH'
    context.commission = 0.0003

def handle_data(datetime, context, data):
    lbt.order('600030.SH', 100, 'buy', 'open')

lbt = LocalBacktest(init_func=initialize, handle_data_func=handle_data)
lbt.run()
print(lbt.summary_result())
print(lbt.summary_trade())