from fastapi import APIRouter, Query
from typing import Union
from typing_extensions import Annotated
from supabase_helpers.supabase_setup import supabase
import json

router = APIRouter(prefix='/trades', tags=["Trades"])

def filter_values(trades, asset_class=None, start=None, end=None, min_price=None, max_price=None, trade_type=None):
    filtered_trades = []
    
    for trade in trades:
        # Filter by asset class
        if asset_class and trade["asset_class"] != asset_class:
            continue
        
        # Filter by start datetime
        if start and trade["trade_date_time"] < start:
            continue
        
        # Filter by end datetime
        if end and trade["trade_date_time"] > end:
            continue
        
        # Filter by min price
        if min_price is not None and trade["TradeDetails"]["price"] < min_price:
            continue
        
        # Filter by max price
        if max_price is not None and trade["TradeDetails"]["price"] > max_price:
            continue
        
        # Filter by trade type
        if trade_type and trade["TradeDetails"]["buySellIndicator"] != trade_type:
            continue
        
        filtered_trades.append(trade)
    
    return filtered_trades

def sort_values(trades, sort_by, ascending):
    if sort_by == 'trade_date_time':
        trades.sort(key=lambda x: x['trade_date_time'], reverse=not ascending)
    elif sort_by == 'price':
        trades.sort(key=lambda x: x['TradeDetails']['price'], reverse=not ascending)
    elif sort_by == 'quantity':
        trades.sort(key=lambda x: x['TradeDetails']['quantity'], reverse=not ascending)
    elif sort_by == 'buySellIndicator':
        trades.sort(key=lambda x: x['TradeDetails']['buySellIndicator'], reverse=not ascending)
    else:
        # Handle invalid sort_by parameter
        raise ValueError(f"Invalid sort_by parameter: {sort_by}")

    return trades

# Get all trades
@router.get("/")
def get_all_trades():
    res = supabase.table('Trade').select('*, TradeDetails(*)').execute()
    return res

# Search Trades
@router.get("/search")
def search_trade(search: str):
    res = supabase.table('Trade').select('*, TradeDetails(*)').execute()
    data = res.json()
    data = json.loads(data)
    result = []
    for val in data["data"]:
        if val["trader"] == search or val["counterparty"] == search or val["instrument_id"] == search or val["instrument_name"] == search:
            result.append(val)
    return result

# Filter trades
@router.get("/filter")
def filter_trades(asset_class: Union[str, None] = None, start: Union[str, None] = None, end: Union[str, None] = None, minPrice: Union[float, None] = None, maxPrice: Union[float, None] = None,  tradeType: Union[str, None] = None):
    res = supabase.table('Trade').select('*, TradeDetails(*)').execute()
    data = res.json()
    data = json.loads(data)
    data = data["data"]
    result = filter_values(data, asset_class=asset_class, start=start, end=end, min_price=minPrice, max_price=maxPrice, trade_type=tradeType)
    return {
        "count": len(result),
        "data": result
    }

# Sort trades
@router.get("/sort")
def sort_trades(sort_by: Annotated[str, Query(title="Sort Parameter", description="Available Parameters to sort from (can select only one at a time): [trade_date_time, price, quantity, buySellIndicator]")], ascending: bool = True):
    res = supabase.table('Trade').select('*, TradeDetails(*)').execute()
    data = res.json()
    data = json.loads(data)
    data = data["data"]
    result = sort_values(data, sort_by=sort_by, ascending=ascending)
    return result

# Get trade by id
@router.get("/{id}")
def get_trade_by_id(id):
    res = supabase.table('Trade').select('*, TradeDetails(*)').eq('trade_id', id).execute()
    return res