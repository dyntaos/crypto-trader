import sys

from Bot import Bot


# If true, don't make trades, just print
simulate = "-s" in sys.argv


print("--- CRYPTO TRADING BOT ---\n")
bot = Bot(sim=simulate)
bot.run()
