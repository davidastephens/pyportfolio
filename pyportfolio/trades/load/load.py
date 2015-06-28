from pyportfolio import Trade, Currency
from pyportfolio.models import TradeList
from pyportfolio.models.models import Security
from pyportfolio.utils.misc import get_required_args
import pandas as pd

def load_csv(file_name):
    df = pd.read_csv(file_name, parse_dates=True)
    tl = trade_from_dataframe(df)
    return tl

def load_excel(file_name):
    df = pd.read_excel(file_name, parse_dates=True)
    tl = trade_from_dataframe(df)
    return tl

def trade_from_dataframe(df):
    tl = TradeList()
    df = df.convert_objects()
    for index, d in df.iterrows():
        d = d.to_dict()
        tl.append(trade_from_dict(d))
    return tl

def trade_from_dict(d):
    #if there is an underlying security, get that
    if not pd.isnull(d['underlying_security_type']):
        ud = get_security_args('underlying', d)
        ud = get_security_args(d['underlying_security_type'].lower(), ud)
        ud['security_type'] = d['underlying_security_type']
        underlying = Security.from_dict(ud)
        d[d['security_type'].lower() + '_' + 'underlying'] = underlying

    #Get security
    ds = get_security_args(d['security_type'].lower(), d)
    ds['security_type'] = d['security_type']
    security = Security.from_dict(ds)
    d['security'] = security

    #Get Currency
    dc = get_security_args('currency', d)
    currency = Currency(**dc)
    d['currency'] = currency

    return Trade(**get_required_args(Trade, d))

def get_security_args(security, d):
    """
    Returns the parameters in d that are prepended with the string in security.
    """
    ud = {}
    for key in d:
        if security + '_' in key:
            if key.startswith(security + '_'):
                ukey = key.replace(security + '_', '')
                ud[ukey] = d[key]
    return ud
