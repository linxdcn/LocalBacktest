from localbacktest.localbacktest import LocalBacktest

def initialize(context):
    print("call handle data")
    context.securities = ['600000.SH']
    context.start_date = '20210301'
    context.end_date = '20210401'
    context.capital = 1000000
    context.benchmark = '000300.SH'
    context.commission = 0.0003

def handle_data(datetime, context, data):
    print("call handle data")

lbt = LocalBacktest(init_func=initialize, handle_data_func=handle_data)
lbt.run()