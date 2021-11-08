import matplotlib.pyplot as plt
import math

class Plotter:

    def __init__(self, num_figs, display_klines=20):
        self.num_figs = num_figs
        self.display_klines = display_klines

        tmp = math.floor(math.sqrt(num_figs))
        self.num_rows = tmp + math.ceil((num_figs - (tmp * tmp)) / tmp)
        self.num_cols = tmp
        self.fig = plt.figure(num_figs)
        self.axes = {}
        plt.ion()

    def update(self, klines, symbol, coin_index):
        subplt_num = int(f"{self.num_rows}{self.num_cols}{coin_index + 1}")
        if subplt_num not in self.axes:
            ax = plt.subplot(subplt_num)
            ax2 = ax.twinx()
            self.axes[subplt_num] = (ax, ax2)
        else:
            ax, ax2 = self.axes[subplt_num]
        ax.clear()
        ax2.clear()

        ax.title.set_text(symbol)

        k = klines.tail(self.display_klines)
        ax.plot(k["close"], color="green")
        ax2.plot(k["close_21_ema"], color="blue")

        # width of candlestick elements
        width = .4
        width2 = .05

        up = k["close"] >= k["open"]
        down = k["close"] < k["open"]

        col1 = 'green'
        col2 = 'red'

        ax.bar(up.index, k["close"] - k["open"], width, bottom=k["open"], color=col1)
        ax.bar(up.index, k["high"] - k["close"], width2, bottom=k["close"], color=col1)
        ax.bar(up.index, k["low"] - k["open"], width2, bottom=k["open"], color=col1)

        ax.bar(down.index, k["close"] - k["open"], width, bottom=k["open"], color=col2)
        ax.bar(down.index, k["high"] - k["open"], width2, bottom=k["open"], color=col2)
        ax.bar(down.index, k["low"] - k["close"], width2, bottom=k["close"], color=col2)

        # rotate x-axis tick labels
        # plt.xticks(rotation=45, ha='right')
        self.draw()
        
        # self.fig.tight_layout()
        plt.show(block=False)

    def draw(self):
        self.fig.tight_layout()
        plt.draw()
        plt.pause(0.001)