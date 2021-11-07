from time import sleep
import datetime

from binance.client import Client

from config import *
from Util import *
from Strategy import calculateIndicators, strategyDecision
from Candlestick import Plotter


class Bot:
    def __init__(self, sim=False):
        self.simulate = sim

        print("- Initializing Bot...")
        if self.simulate:
            print("<< SIMULATING: No trades will be made >>")
        self.client = Client(API, SECRET)
        print("- Loaded API keys")

        self.plt = Plotter(len(markets))
        self.usdt = 0
        self.position_val = 0
        self.balance = []
        self.bought = {}
        self.ticks = {}
        self.available_currencies = []
        self.refreshBalance()
        print('- Done fetching balance')
        print('- Generating bought/sold statuses...')
        self.generateBoughtStatus()
        self.generateTicks()
        print(f'- Balance: {self.usdt:.4f} {base_currency}')

    def run(self):
        iterations = 0
        print(f"{datetime.datetime.now()}: ", end="")
        print("- Bot is running")
        print('\n--------TRADES-------\n')
        while True:
            try:
                if self.simulate and iterations % sim_msg_display_cycles == sim_msg_display_cycles - 1: 
                    print("<< SIMULATING: No trades are being made >>")
                if iterations % holdings_update_cycles == holdings_update_cycles - 1:

                    temp_base_balance = self.usdt
                    self.refreshBalance()
                    self.generateBoughtStatus()
                    if temp_base_balance !=  self.usdt:
                        print(f'- Balance: {self.usdt:.4f} {base_currency}')

                for coin in markets:
                    symbol = coin + base_currency
                    klines = self.getKlines(symbol)

                    indicators = calculateIndicators(klines)
                    enterLong, exitLong = strategyDecision(*indicators)
                    self.plt.update(klines, symbol, markets.index(coin))

                    if self.bought[symbol]:
                        if exitLong:
                            self.sell(symbol, klines)
                    else:
                        if enterLong:
                            self.buy(symbol, klines)

                sleep(30)
            except Exception as ex:
                print(ex) 
                sleep(10)
            iterations += 1


    def generateBoughtStatus(self):
        for coin in markets:
            coin += base_currency
            symbol_orders = self.client.get_all_orders(symbol=coin, limit=1)

            if len(symbol_orders) > 0 and symbol_orders[0]['side'] == 'BUY' and symbol_orders[0]['status'] == 'FILLED':
                print(f"{datetime.datetime.now()}: ", end="")
                print(f'- {coin} is currently holding long')
                self.bought[coin] = symbol_orders[0]
            else:
                self.bought[coin] = None

    def buy(self, symbol, df):
        self.refreshBalance()

        if self.usdt > 10:
            price = df["close"][len(df) - 1]
            amount = self.usdt/price
            amount = truncate(amount, self.ticks[symbol])

            if not self.simulate:
                print(f"{datetime.datetime.now()}: ", end="")
                print(f'Buying {amount} {symbol} @ {price} {base_currency}...')
                buy_market = self.client.order_market_buy(symbol=symbol, quoteOrderQty=self.usdt)
                self.bought[symbol] = buy_market

            # Simulate
            else:
                print(f"{datetime.datetime.now()}: ", end="")
                print(f'SIM: Buying {amount} {symbol} @ {price} {base_currency}...')
                buy_market = self.client.create_test_order(
                    symbol=symbol, side='BUY', type='MARKET', quoteOrderQty=self.usdt)

                self.bought[symbol] = {
                    'type': 'BUY',
                    'cummulativeQuoteQty': self.usdt,
                    'executedQty': amount
                }

        else:
            if not any(self.bought.values()):
                print(f"{datetime.datetime.now()}: ", end="")
                print(f"Buy signal on {symbol}")
                print(f"{datetime.datetime.now()}: ", end="")
                print(f"{symbol} | Not enough {base_currency} to trade (minimum of $10)")

    def sell(self, symbol, df):
        self.refreshBalance()

        symbol_balance = 0
        for s in self.balance:
            if s['asset'] + base_currency == symbol:
                symbol_balance = s['free']

        # TESTING
        #symbol_balance = self.bought[symbol]['executedQty']
        ###

        price = df["close"][len(df) - 1]

        if symbol_balance * price > 10:

            amount = truncate(symbol_balance, self.ticks[symbol])

            if not self.simulate:
                print(f"{datetime.datetime.now()}: ", end="")
                print(f'Selling {amount} {symbol} @ {price} {base_currency}...')
                sell_market = self.client.order_market_sell(symbol=symbol, quantity=amount)

            else:
                print(f"{datetime.datetime.now()}: ", end="")
                print(f'SIM: Selling {amount} {symbol} @ {price} {base_currency}...')
                sell_market = self.client.create_test_order(
                    symbol=symbol, side='SELL', type='MARKET', quantity=amount)

                sell_market = {
                    'cummulativeQuoteQty': amount * price
                }

            net = float(sell_market['cummulativeQuoteQty']) - float(self.bought[symbol]['cummulativeQuoteQty'])
            print(f'Net profit: {net} {base_currency}\n')

            self.bought[symbol] = None

        else:
            if not any(self.bought.values()):
                print(f"{datetime.datetime.now()}: ", end="")
                print(f"Sell signal on {symbol}")
                print(f"{datetime.datetime.now()}: ", end="")
                print(f"Not enough {symbol} to trade (minimum of $10)")

    def generateTicks(self):
        print('- Generating symbol step sizes...')
        try:
            ticks = openPickle('Ticks.pickle')
            print('- Loading ticks from file')
            self.ticks = ticks
        except Exception as ex:
            print(ex)
            for coin in markets:
                coin += base_currency
                self.getSymbolPrecision(coin)
            savePickle(self.ticks, 'Ticks.pickle')

    def getSymbolPrecision(self, symbol):
        for filt in self.client.get_symbol_info(symbol=symbol)['filters']:
            if filt['filterType'] == 'LOT_SIZE':
                diff = filt['stepSize'].find('1') - filt['stepSize'].find('.')
                self.ticks[symbol] = max(diff, 0)
                break

    def getKlines(self, symbol):
        raw_klines = self.client.get_klines(
            symbol=symbol, interval=tick_interval)
        return binanceToStockDataFrame(raw_klines)

    def refreshBalance(self):
        balance = self.client.get_account()["balances"]
        if balance is not None:
            self.available_currencies = []
            self.balance = []
            for dict in balance:
                dict["free"] = float(dict["free"])
                dict["locked"] = float(dict["locked"])

                if dict['asset'] == base_currency:
                    self.usdt = float(dict["free"])
                elif (dict["free"] > 0.0):
                    dict["asset"] = dict["asset"]
                    self.available_currencies.append(dict["asset"])
                    self.balance.append(dict)
