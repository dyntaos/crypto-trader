from pandas.core import indexing
from config import *


def strategyDecision(*args):
    indicators = [x.iloc[-1] for x in args]
    return strategyCalculator(*indicators)


def strategyCalculator(kdj_cross_up, kdj_cross_down):

    # KDJ J/D cross-over
    longKdjCrossCondition = kdj_cross_up
    exitLongKdjCondition = kdj_cross_down

    # STRAT
    enterLongCondition = longKdjCrossCondition
    exitLongCondition = exitLongKdjCondition

    return (enterLongCondition, exitLongCondition)


def calculateIndicators(klines):
    kdj_j_cross_up_d = klines["kdjj_{}_xu_kdjd_{}".format(kdj_moving_avg, kdj_moving_avg)]
    kdj_j_cross_down_d = klines["kdjj_{}_xd_kdjd_{}".format(kdj_moving_avg, kdj_moving_avg)]

    return (kdj_j_cross_up_d, kdj_j_cross_down_d)
