from typing import Type

from app.schemas import Candle, BacktestResult
from app.strategies import Strategy


class Backtest:

    def __init__(self, data: list[Candle], strategy: Type[Strategy]):
        self.data = data
        self.strategy = strategy

    def run(self) -> BacktestResult:
        result = self.strategy().run_backtest(self.data)
        return result
