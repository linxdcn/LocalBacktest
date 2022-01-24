from localbacktest import *

def initialize(context):
    print("call handle data")
    context.securities = ['600000.SH']
    context.start_date = '2021-03-01'
    context.end_date = '2021-04-01'
    context.capital = 100000
    context.benchmark = '000300.SH'
    context.commission = 0.0003

def handle_data(datetime, context, data):
    print("call handle data")

lbt = LocalBacktest(init_func=initialize, handle_data_func=handle_data)
lbt.run()