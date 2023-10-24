from .abstract import Strategy
from app.schemas import Candle, BacktestResult


class MACDStrategy(Strategy):

    def __init__(self):
        ...

    def run_backtest(self, data: list[Candle]) -> BacktestResult:
        ...
