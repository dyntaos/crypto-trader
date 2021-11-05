import pandas as pd
import numpy as np
import math
import pickle
import stockstats


def binanceToStockDataFrame(klines):
    klines = np.array(klines).reshape(-1, 12)
    df = pd.DataFrame(klines, dtype=float, columns=('Open Time',
                                                    'open',
                                                    'high',
                                                    'low',
                                                    'close',
                                                    'volume',
                                                    'Close time',
                                                    'Quote asset volume',
                                                    'amount',
                                                    'Taker buy base asset volume',
                                                    'Taker buy quote asset volume',
                                                    'Ignore'))
    df['Open Time'] = pd.to_datetime(df['Open Time'], unit='ms')
    df.set_index("Open Time")
    df = stockstats.StockDataFrame(df)
    return df


def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper


def savePickle(var, file_name):
    outfile = open(file_name, 'wb')
    pickle.dump(var, outfile)

    outfile.close()


def openPickle(file_name):
    outfile = open(file_name, 'rb')
    df = pickle.load(outfile)

    outfile.close()

    return df
