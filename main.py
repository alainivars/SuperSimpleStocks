#!/usr/bin/env python3
#
# python 3 example of resolve the :
# Assignment – Super Simple Stocks
#
# Author: Alain IVARS (alainivars@gmail.com) SkypeId: highfeature
# Copyright 2017 Alain IVARS All rights reserved
# Licence: GPLv2
#

"""
This is a point of view of an Architect ... and here you can see how clear specifications are vitals to avoid
misunderstand with the customer.
An other important point: set random start positions in specification broke the repeatability of the validation
Other points: "NEVER RE-INVENT THE WHELL" and "KEEP IT SIMPLE, STUPID"
Last point on PEP8: I like all the recommendations in this PEP except one, the limit of 79 characters by line
for me that an antediluvian thing when screen had only 80 characters by line, now in the 21st century, every editors
even vi can display up to 120 characters by line and I use that, that make the code more readable, specialy when
I see some lines cutted in 10 sub-lines with backslash at end, that remind me some obscur codes
than I had to debug. You can agree or not, you have the right, this is my opinion, of course when I work for a client
I am its coding rules and these can be very different from one to another.

Assumptions for that program; because I don't have time:

- in 2 hours MAX (In my case: one hour of analyze and one hour of coding)
- just transform draft specification paper to reel SPEC in "Super Simple Stocks Requirements.odt"
- No database
- No GUI
- No TDD development
- No dependencies/requirement file
- No Deployement system
- Not designed for re-use
- No unit/functional tests
- No continuous integration system in use
- Data in are static, create 10 buy lines
- No documentations

For examples of previews items, please look in my other open sources projects.

Command line:

python3 main.py

Output:

                                        Common            Preferred
           Dividend Yield  0.12883333333333336                  0.1
                P/E Ratio    8.584866220735787                 12.5
           Geometric Mean        1778.07337785        1584.48546491
              Stock Price              13170.0               4800.0

"""

from datetime import datetime, timedelta
from enum import Enum
from time import sleep
from scipy.stats.mstats import gmean


class Item(Enum):
    TEA = 1
    POP = 2
    ALE = 3
    GIN = 4
    JOE = 5


class Type(Enum):
    Common = 1
    Preferred = 2


class DataIn(Enum):
    StockSymbol = 0
    TheType = 1
    LastDividend = 2
    FixedDividend = 3
    ParValue = 4


class Formula(Enum):
    DividendYield = 1
    PERatio = 2
    GeometricMean = 3
    StockPrice = 4

dataIn = (
    ("Stock Symbol", "Type", "Last Dividend", "Fixed Dividend", "Par Value"),
    (Item.TEA, Type.Common,    0.0,              0.0,                100.0),
    (Item.POP, Type.Common,    8.0,              0.0,                100.0),
    (Item.ALE, Type.Common,   23.0,              0.0,                 60.0),
    (Item.GIN, Type.Preferred, 8.0,              0.02,               100.0),
    (Item.JOE, Type.Common,   13.0,              0.0,                250.0)
)

formula = [
    ["", "Common", "Preferred"],
    ["Dividend Yield", 0.0, 0.0],
    ["P/E Ratio", 0.0, 0.0],
    ["Geometric Mean", 0.0, 0.0],
    ["Stock Price", 0.0, 0.0],
]
trades_item_symbol = [
    Item.TEA, Item.POP, Item.ALE, Item.GIN, Item.JOE,
    Item.TEA, Item.POP, Item.GIN, Item.GIN, Item.JOE
]
trades_item_type = [
    Type.Common, Type.Common, Type.Common, Type.Preferred, Type.Common,
    Type.Common, Type.Common, Type.Preferred, Type.Preferred, Type.Common
]
record_format = {
    "StockId": None,
    "TypeId": None,
    "timestamp": 0.0,
    "quantity": 0,
    "buy": None,
    "price": 0.0
}


def add_some_trade_record():
    """Record a trade, with timestamp, quantity of shares, buy or sell indicator and price"""
    trades = []
    for num in range(10):
        trade = dict(record_format)
        trade["timestamp"] = datetime.now() - timedelta(minutes=14, seconds=59)
        trade["StockId"] = trades_item_symbol[num]
        trade["TypeId"] = trades_item_type[num]
        trade["quantity"] = 10 + num
        trade["buy"] = True
        trade["price"] = dataIn[trade["StockId"].value][DataIn.ParValue.value] * trade["quantity"]
        trades.append(trade)
        sleep(0.2)
    return trades


def calculate_the_dividend_yield():
    """calculate the dividend yield"""
    count_comon, count_prefered = 0, 0

    for item in dataIn[1:]:

        if item[DataIn.TheType.value] == Type.Common:
            count_comon += 1
            cur_dividended_yield = item[DataIn.LastDividend.value] / item[DataIn.ParValue.value]
            formula[Formula.DividendYield.value][Type.Common.value] += cur_dividended_yield

        else:
            count_prefered += 1
            cur_dividended_yield = item[DataIn.LastDividend.value] / item[DataIn.ParValue.value]
            cur_dividended_yield += item[DataIn.FixedDividend.value]
            formula[Formula.DividendYield.value][Type.Preferred.value] += cur_dividended_yield

    formula[Formula.DividendYield.value][Type.Common.value] /= count_comon
    formula[Formula.DividendYield.value][Type.Preferred.value] /= count_prefered


def calculate_the_per():
    """calculate the P/E Ratio"""
    count = 0
    for item in dataIn[1:]:
        if item[DataIn.TheType.value] == Type.Common:
            count += 1
            if item[DataIn.LastDividend.value]:
                cur_dividended_yield = item[DataIn.ParValue.value] / item[DataIn.LastDividend.value]
            else:
                cur_dividended_yield = 0
            formula[Formula.PERatio.value][Type.Common.value] += cur_dividended_yield
        else:
            cur_dividended_yield = item[DataIn.ParValue.value] / item[DataIn.LastDividend.value]
            formula[Formula.PERatio.value][Type.Preferred.value] += cur_dividended_yield
    formula[Formula.PERatio.value][Type.Common.value] /= count


def calculate_stock_price_based_on_trades_recorded_in_past_15_minutes(start_time):
    """Calculate Stock Price based on trades recorded in past 15 minutes"""
    liste = [trade for trade in trades if trade["timestamp"] >= start_time]
    for item in liste:
        formula[Formula.StockPrice.value][dataIn[item["StockId"].value][DataIn.TheType.value].value] += item["price"]


def get_prices(trades, start_time, type):
    """prices for all stocks of type 'type'"""
    return [trade["price"] for trade in trades if trade["timestamp"] >= start_time and trade["TypeId"] == type]


def calculate_the_gbce_all_share_index_using_the_geometric_mean_of_prices_for_all_stocks(trades, start_time):
    """Calculate the GBCE All Share Index using the geometric mean of prices for all stocks"""
    all_prices_common = get_prices(trades, start_time, Type.Common)
    formula[Formula.GeometricMean.value][Type.Common.value] = gmean(all_prices_common)
    all_prices_prefered = get_prices(trades, start_time, Type.Preferred)
    formula[Formula.GeometricMean.value][Type.Preferred.value] = gmean(all_prices_prefered)


if __name__ == "__main__":

    trades = add_some_trade_record()
    calculate_the_dividend_yield()
    calculate_the_per()
    start_time = datetime.now() - timedelta(minutes=15)
    calculate_stock_price_based_on_trades_recorded_in_past_15_minutes(start_time)
    calculate_the_gbce_all_share_index_using_the_geometric_mean_of_prices_for_all_stocks(trades, start_time)
    print("\n")
    for line in formula:
        print("%25s %20s %20s" % (line[0], line[1], line[2]))

    exit(0)
