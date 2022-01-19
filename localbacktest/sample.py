from localbacktest.localbacktest import LocalBacktest

def initialize(context):
    print("call initialize")

def handle_data(bar_datetime, context, bar_data):
    print("call handle data")

lbt = LocalBacktest
res = lbt.run()