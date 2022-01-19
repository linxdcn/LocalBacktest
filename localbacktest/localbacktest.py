
from sqlalchemy import null


class Context():
    pass

class LocalBacktest():

    def __init__(self, init_func, handle_data_func):
        context = Context()
        context.capital = 1000
        self._context = context
        self._init_func = init_func
        self._handle_data_func = handle_data_func

    def run(self):
        self._init_func(null)
        for i in range(5):
            self._handle_data_func(null, null, null)
            
