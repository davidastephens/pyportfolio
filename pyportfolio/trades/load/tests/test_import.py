import unittest
from pyportfolio.models import TradeList
from pyportfolio.trades.load import csv
from pyportfolio.utils.testing import get_data_path


class TestImport(unittest.TestCase):
    def test_csv(self):
        trade_list = csv.load_file(get_data_path() + 'test.csv')
        self.assertIsInstance(trade_list, TradeList)
        #trade_list.to_csv(get_data_path() + 'out.csv')
