from abc import ABC, abstractmethod

import pandas as pd


class Strategy(ABC):

    @abstractmethod
    def run_backtest(self, data: pd.DataFrame):
        ...
