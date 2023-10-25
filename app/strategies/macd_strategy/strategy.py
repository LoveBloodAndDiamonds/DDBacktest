import pandas as pd
import talib

from .draw_chart import plot_chart
from ..abstract import Strategy
from ...configuration import logger


class MACDStrategy(Strategy):

    def __init__(self):
        ...

    def run_backtest(self, data: pd.DataFrame):
        self.calculate_pump(data)
        self.calculate_macd(data)
        self.calculate_hist_signal(data)
        self.calculate_macd_signal_short(data)

        plots_data = self.test_strategy(data)
        counts = data['result'].value_counts()
        take_profit_count = counts.get('take_profit', 0)
        stop_loss_count = counts.get('stop_loss', 0)
        logger.success(f"Result:\n"
                       f"TP : {take_profit_count}\n"
                       f"SL : {stop_loss_count}\n"
                       f"TP*: {take_profit_count}\n"
                       f"SL*: {stop_loss_count}\n"
                       f"WR%: {take_profit_count/(stop_loss_count+take_profit_count)}\n")

        if input("Type anything to plot charts:"):
            for plt in plots_data:
                plot_chart(plt)

    @classmethod
    def calculate_pump(cls, data: pd.DataFrame):
        data['is_pump'] = False
        for index, row in data.iterrows():
            pump_size = cls.check_pump_size(row)
            if pump_size > 2:
                data.at[index, 'is_pump'] = True

    @classmethod
    def check_pump_size(cls, c: pd.Series) -> bool:
        return ((c['high'] / c['open']) - 1) * 100

    @classmethod
    def calculate_macd(cls, data: pd.DataFrame):
        macd, signal, hist = talib.MACD(data['close'], fastperiod=6, slowperiod=13, signalperiod=9)
        data['macd'] = macd
        data['signal'] = signal
        data['histogram'] = hist

    @classmethod
    def calculate_hist_signal(cls, data: pd.DataFrame):
        data['hist_signal'] = False  # Создаем новый столбец is_signal и заполняем его значением False

        pump_rows = data[data['is_pump']]

        for index, row in pump_rows.iterrows():
            histogram = row['histogram']
            for i, r in data.iloc[index:].iterrows():
                if r["histogram"] < histogram:
                    data.at[i, "hist_signal"] = True
                    break
                elif r["histogram"] > histogram:
                    histogram = r["histogram"]

    @classmethod
    def calculate_macd_signal_short(cls, data: pd.DataFrame):
        data['macd_signal_short'] = False

        pump_rows = data[data['is_pump']]
        for index, row in pump_rows.iterrows():
            _macd = row["macd"]
            _signal = row["signal"]
            if _macd < _signal:  # delete wring signals
                continue

            for i, r in data.iloc[index:].iterrows():
                macd = r["macd"]
                signal = r["signal"]
                if macd < signal:
                    data.at[i, "macd_signal_short"] = True
                    break

    @classmethod
    def test_strategy(cls, data: pd.DataFrame):
        data["result"] = None
        signal_rows = data[data["hist_signal"]]

        plots_data = list()
        start_index = 0
        for index, row in signal_rows.iterrows():

            if index > start_index:

                start_index = index
                open_price = row["close"]
                stop_loss = open_price * 1.03
                take_profit = open_price * 0.9

                for i, r in data.iloc[index + 1:].iterrows():
                    if r["high"] > stop_loss:
                        data.at[index, "result"] = "stop_loss"
                        plots_data.append(data.iloc[start_index - 20: i+2])
                        start_index = i
                        break
                    elif r["low"] < take_profit:
                        data.at[index, "result"] = "take_profit"
                        plots_data.append(data.iloc[start_index - 20: i + 2])
                        start_index = i
                        break

        return plots_data
