import csv
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from typing import List

from app.schemas import Candle


def parse_csv(path: str):
    csv_data = _read_csv(path)
    validated_candles = _validate_candles(csv_data)
    return validated_candles


def _read_csv(path: str) -> list:
    with open(path, "r") as file:
        return list(csv.reader(file))[1:]


def _validate_candles(candles: List) -> List[Candle]:
    def validate_candle(index, c):
        timestamp = int(c[0])
        return Candle(
            timestamp=timestamp,
            datetime=datetime.fromtimestamp(timestamp / 1000),
            open=float(c[1]),
            high=float(c[2]),
            low=float(c[3]),
            close=float(c[4]),
            index=index
        )

    with ThreadPoolExecutor() as executor:
        validated_candles = list(executor.map(validate_candle, range(len(candles)), candles))

    return validated_candles
