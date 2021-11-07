import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from config import *


def strategyDecision(*args):
    kdj_d, kdj_j, kdj_j_slope, kdj_j_cross_up_d, kdj_j_cross_down_d, ma21, ma21_slope = args

    kdj_d = kdj_d.iloc[-1]
    kdj_j = kdj_j.iloc[-1]
    kdj_j_slope = kdj_j_slope.iloc[-1][0]
    kdj_j_cross_up_d = kdj_j_cross_up_d.iloc[-1]
    kdj_j_cross_down_d = kdj_j_cross_down_d.iloc[-1]
    ma21 = ma21.iloc[-1]
    ma21_slope = ma21_slope.iloc[-1][0]

    return strategyCalculator(kdj_d, kdj_j, kdj_j_slope, kdj_j_cross_up_d, kdj_j_cross_down_d, ma21, ma21_slope)


def strategyCalculator(kdj_d, kdj_j, kdj_j_slope, kdj_cross_up, kdj_cross_down, ma21, ma21_slope):

    # KDJ J Instantaneous Slope
    longKdjInstantSlope = kdj_j_slope > kdj_j_instant_slope_lower_threshold

    # KDJ J/D cross-over
    longKdjCrossCondition = kdj_cross_up
    exitLongKdjCondition = kdj_cross_down

    # KDJ J MA21 Slope
    longKdjJMa21Slope = ma21_slope > kdj_j_ma21_slope_lower_threshold

    # STRAT
    enterLongCondition = longKdjCrossCondition and longKdjInstantSlope and longKdjJMa21Slope
    exitLongCondition = exitLongKdjCondition

    return (enterLongCondition, exitLongCondition)


def calculateIndicators(klines):
    kdj_d = klines["kdjd_{}".format(kdj_moving_avg)]

    kdj_j = klines["kdjj_{}".format(kdj_moving_avg)]
    kdj_j_slope = pd.DataFrame(np.diff(kdj_j))
    kdj_j_cross_up_d = klines["kdjj_{}_xu_kdjd_{}".format(kdj_moving_avg, kdj_moving_avg)]
    kdj_j_cross_down_d = klines["kdjj_{}_xd_kdjd_{}".format(kdj_moving_avg, kdj_moving_avg)]

    ma21 = klines["kdjj_21_ema"]
    ma21_slope = pd.DataFrame(np.diff(ma21))

    return (kdj_d, kdj_j, kdj_j_slope, kdj_j_cross_up_d, kdj_j_cross_down_d, ma21, ma21_slope)
