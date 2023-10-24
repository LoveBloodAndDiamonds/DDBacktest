from datetime import datetime

from pydantic import BaseModel


class Candle(BaseModel):
    timestamp: int
    datetime: datetime
    open: float
    high: float
    low: float
    close: float
    index: int

    def __str__(self):
        return f'{self.datetime.strftime("%d.%m %H:%M")}| ' \
               f'o:{self.open}| ' \
               f'h:{self.high}| ' \
               f'l:{self.low}| ' \
               f'c:{self.close}| ' \
               f'i:{self.index}|'
