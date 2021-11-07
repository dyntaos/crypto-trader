import os
from binance.client import Client

from dotenv import load_dotenv
load_dotenv()


API = os.getenv("API")
SECRET = os.getenv("SECRET")

# markets = ['SHIB','ETH','BNB','DOGE','ADA','UNI','LTC','BTC']
markets = ['SHIB','ETH','BNB','DOGE','SOL','UNI','LTC','BTC']
tick_interval = Client.KLINE_INTERVAL_30MINUTE
base_currency = 'USDT'
kdj_moving_avg = 5

# Update currency holdings every N cycles
holdings_update_cycles = 2
sim_msg_display_cycles = 15

kdj_j_ma21_slope_lower_threshold = 0.05
kdj_j_instant_slope_lower_threshold = 12.0
