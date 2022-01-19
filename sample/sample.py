from localbacktest.localbacktest import LocalBacktest

def initialize(context):
    print("call initialize")

def handle_data(context, datetime, bar_data):
    print("call handle data")

lbt = LocalBacktest(init_func=initialize, handle_data_func=handle_data)
lbt.run()