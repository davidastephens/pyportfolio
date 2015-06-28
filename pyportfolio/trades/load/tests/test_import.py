import unittest
from pyportfolio.models import TradeList
from pyportfolio.trades.load import load
from pyportfolio.utils.testing import get_data_path


class TestImport(unittest.TestCase):
    def test_csv(self):
        trade_list = load.load_csv(get_data_path() + 'test.csv')
        self.assertIsInstance(trade_list, TradeList)
        #trade_list.to_csv(get_data_path() + 'out.csv')

    def test_excel(self):
        trade_list = load.load_excel(get_data_path() + 'test.xlsx')
        self.assertIsInstance(trade_list, TradeList)
        trade_list.to_csv(get_data_path() + 'out.csv')
