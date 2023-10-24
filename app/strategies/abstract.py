from abc import ABC, abstractmethod

from app.schemas import Candle, BacktestResult


class Strategy(ABC):

    @abstractmethod
    def run_backtest(self, data: list[Candle]) -> BacktestResult:
        ...
