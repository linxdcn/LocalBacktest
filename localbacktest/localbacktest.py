
from sqlalchemy import null


class LocalBacktest():

    def __init__(self, init_func, handle_data_func):
        self._init_func = init_func
        self._handle_data_func = handle_data_func

    def run(self):
        self._init_func(null)
        for i in range(5):
            self.run()
            
