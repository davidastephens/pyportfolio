import csv
from pyportfolio.utils.misc import get_required_args
import pandas as pd

fieldnames = [
    'account',
    'amount',
    'price',
    'commission',
    'currency_name',
    'equity_ticker',
    'security_type',
    'underlying_security_type',
    'underlying_equity_ticker',
    'option_strike',
    'option_type',
    'option_expiry',
    ]

class Security(object):
    def __hash__(self):
        return hash(self._key)

    def __eq__(self, other):
        return self._key == other._key

    @classmethod
    def from_dict(cls, d):
        constructor = cls.factory(d['security_type'])
        return constructor(**get_required_args(constructor.__init__, d))

    @staticmethod
    def factory(type):
        if type == "Equity":
            return Equity
        elif type == "Option":
            return Option
        elif type == "Future":
            return Future
        elif type == "Index":
            return Index
        elif type == "Commodity":
            return Commodity

class Equity(Security):
    def __init__(self, ticker):
        self.ticker = ticker

    @property
    def _key(self):
        return self.ticker

    def to_dict(self):
        d = {}
        d['equity_ticker'] = self.ticker
        d['security_type'] = self.__class__.__name__
        return d

class Option(Security):
    def __init__(self, underlying, expiry, strike, type):
        self.underlying = underlying
        self.expiry = pd.to_datetime(expiry).date()
        self.strike = strike
        self.type = type

    @property
    def _key(self):
        return (self.underlying, self.expiry, self.strike, self.type)

    def to_dict(self):
        d = {}
        d['security_type'] = self.__class__.__name__
        underlying_d = self.underlying.to_dict()
        d['option_type'] = self.type
        d['option_strike'] = self.strike
        d['option_expiry'] = self.expiry
        for key in underlying_d:
            d['underlying_' + key] = underlying_d[key]
        return d


class Future(Security):
    def __init__(self, underlying, expiry):
        self.underlying = underlying
        self.expiry = expiry

    def __eq__(self, other):
        return self.underlying == other.underlying & self.expiry == other.expiry


class Index(Security):
    pass


class Commodity(Security):
    def __init__(self, name):
        self.name = name


class Currency(object):
    def __init__(self, name):
        self.name = name

    def to_dict(self):
        d = {}
        d['currency_name'] = self.name
        return d


class Account(object):
    def __init__(self, name):
        self.name = name
        self.trades = TradeList()

    def add_trade(self, trade):
        self.trades.add_trade(trade)

    @property
    def positions(self):
        return self.trades.positions


class Trade(object):
    def __init__(self, security, amount, price, commission, currency):
        self.security = security
        self.amount = amount
        self.price = price
        self.commission = commission
        self.currency = currency

    @property
    def value(self):
        "Amount of the trade, excluding commissions"
        return self.price * self.amount

    @property
    def net_value(self):
        "Amount of the trade, including commissions"
        return self.price * self.amount + self.commission

    def to_dict(self):
        d = {}
        d.update(self.security.to_dict())
        d['amount'] = self.amount
        d['price'] = self.price
        d['commission'] = self.commission
        d.update(self.currency.to_dict())
        return d

class Position(object):
    "Position object, contains amount of stock, cost basis"
    def __init__(self, security, amount, cost_basis):
        self.security = security
        self.amount = amount
        self.cost_basis = cost_basis

    def __add__(self, other):
        if self.security == other.security:
            return Position(security=self.security,
                            amount=self.amount + other.amount,
                            cost_basis=self.cost_basis + other.cost_basis)
        else:
            raise AttributeError("Can't add positions of different securities")

    @classmethod
    def from_trade(cls, trade):
        ##TODO: What about currency?
        return cls(security=trade.security, amount=trade.amount,
                   cost_basis=trade.net_value)

    def add_trade(self, trade):
        if self.security == trade.security:
            self.amount = self.amount + trade.amount
            ##TODO: Cost basis isn't that simple?
            ##TODO: What about currency?
            self.cost_basis = self.net_value
        else:
            raise AttributeError("Can't add positions of different securities")


class TradeList(list):
    """
    List of trades
    """
    def add_trade(self, trade):
        self.append(trade)

    @property
    def positions(self):
        return self._get_positions()

    def _get_positions(self):
        """
        Returns dict of positions
        """
        positions = {}
        for trade in self:
            position = positions.get(trade.security, None)
            if position:
                position.add_trade(trade)
            else:
                position = Position.from_trade(trade)
                positions[trade.security] = position
        return positions

    def to_dicts(self):
        return [trade.to_dict() for trade in self]

    def to_csv(self, file_name):
        print(fieldnames)
        with open(file_name, 'w') as out_file:
            writer = csv.DictWriter(out_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.to_dicts())

