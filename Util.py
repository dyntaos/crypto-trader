import pandas as pd
import numpy as np
import math
import pickle
import stockstats


def binanceToStockDataFrame(klines):
    klines = np.array(klines).reshape(-1, 12)
    df = pd.DataFrame(klines, dtype=float, columns=('open time',
                                                    'open',
                                                    'high',
                                                    'low',
                                                    'close',
                                                    'volume',
                                                    'close time',
                                                    'quote asset volume',
                                                    'amount',
                                                    'taker buy base asset volume',
                                                    'taker buy quote asset volume',
                                                    'ignore'))
    df['open time'] = pd.to_datetime(df['open time'], unit='ms')
    df.set_index("open time")
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
