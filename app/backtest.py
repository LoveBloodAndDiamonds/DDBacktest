from typing import Type

import pandas as pd

from app.strategies import Strategy


class Backtest:

    def __init__(self, data: pd.DataFrame, strategy: Type[Strategy]):
        self.data = data
        self.strategy = strategy

    def run(self) -> pd.DataFrame:
        result = self.strategy().run_backtest(self.data)
        return result
