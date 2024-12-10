import sys
sys.path.insert(0, '../TradeTransactionsSort')

from tests.test_python.test_utility import TestUtility
from tests.test_python.test_csv_handling import TestCSVHandling
from tests.test_python.test_update_trades import TestUpdateTrades
import pytest

__all__ = ['TestCSVHandling', 'TestUpdateTrades', 'TestUtility', 'test_main']

class RunTests():
    def __init__(self):
        pass

    def run_tests(self):
        #pytest.main(['-k', __all__[2], '-v'])
        for module in __all__:
            args = ['-k', module, '-v']
            pytest.main(args)