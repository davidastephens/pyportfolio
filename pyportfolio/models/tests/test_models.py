from pyportfolio.models import Stock, Option, Future, Account, Trade, Commodity, Index, Currency, TradeList
from datetime import date
import unittest

AAPL = Stock(ticker='AAPL')
AAPL_option = Option(underlying=AAPL, expiry=date(2016, 6, 30), strike=105, type='call')
copper = Commodity(name='Copper')
cu_future = Future(underlying=copper, expiry=date(2020, 6, 30))
USD = Currency(name='USD')
trade = Trade(security=AAPL, amount=100, price=120, commission=7.99, currency=USD)
account = Account(name='Test Account')
account.add_trade(trade)
option_trade = Trade(security=AAPL_option, amount=100, price=20, commission=7.99, currency=USD)

class TestModels(unittest.TestCase):
    def test_account(self):
        self.assertEquals(account.positions[AAPL].amount, 100)

    def test_trade(self):
        self.assertEquals(trade.value, 100*120)
        self.assertEquals(trade.commission, 7.99)


class TestCollections(unittest.TestCase):
    def test_positions(self):
        tl = TradeList()
        tl.add_trade(trade)
        self.assertEquals(tl.positions[AAPL].amount, 100)
        self.assertEquals(tl.positions[AAPL].cost_basis, 100 * 120 + 7.99)

    def test_to_csv(self):
        tl = TradeList()
        tl.add_trade(trade)
        tl.add_trade(option_trade)
        #tl.to_csv('test.csv')


