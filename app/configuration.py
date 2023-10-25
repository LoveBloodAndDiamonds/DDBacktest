__all__ = ("conf", "logger",)

import sys
from typing import Literal

import pendulum
import toml
from loguru import logger
from pydantic import BaseModel


class BaseConf(BaseModel):
    symbol: str
    interval: str


class LogsConf(BaseModel):
    path: str | bool
    level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class BacktestRanges(BaseModel):
    start_year: int
    strat_month: int
    end_year: int
    end_month: int


class Configuration(BaseModel):
    base_conf: BaseConf
    backtest_ranges: BacktestRanges
    logs_conf: LogsConf


class LoguruConfiguration:
    @classmethod
    def set_datetime(cls, record):
        """Set local datetime."""
        record["extra"]["datetime"] = pendulum.now("Europe/Moscow")

    @classmethod
    def get_logger(cls,
                   logs_path: str = "logs/app.log",
                   level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "DEBUG"):
        """
        :param level:
        :param logs_path: Can be empty, so logs will not write to file
        :return:
        """
        logger.remove()
        logger.configure(patcher=cls.set_datetime)
        if logs_path:
            logger.add(logs_path,
                       format="<white>{extra[datetime]:%d.%m %H:%M:%S.%f}</white> | "
                              "<level>{level}</level>| "
                              "|{name} {function} line:{line}| "
                              "<bold>{message}</bold>",
                       rotation="10 MB",
                       compression='zip')
        logger.add(sys.stderr, level=level,
                   format="<white>{extra[datetime]:%d.%m %H:%M:%S.%f}</white>|"
                          "<level>{level}</level>|"
                          "<bold>{message}</bold>",
                   )
        return logger


with open("config.toml", 'r') as file:
    conf = Configuration.model_validate(toml.load(file))

logger = LoguruConfiguration.get_logger(  # noqa
    logs_path=conf.logs_conf.path,
    level=conf.logs_conf.level
)
