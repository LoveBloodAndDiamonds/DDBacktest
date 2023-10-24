__all__ = ("conf", "logger",)

import sys

import pendulum
from loguru import logger
from pydantic import BaseModel
import toml


class Base(BaseModel):
    symbol: str
    interval: str

    start_year: int
    strat_month: int
    end_year: int
    end_month: int


class Configuration(BaseModel):
    base: Base


class LoguruConfiguration:
    @classmethod
    def set_datetime(cls, record):
        """Set local datetime."""
        record["extra"]["datetime"] = pendulum.now("Europe/Moscow")

    @classmethod
    def get_logger(cls, logs_path: str = "logs/app.log"):
        """
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
        logger.add(sys.stderr, level="DEBUG",
                   format="<white>{extra[datetime]:%d.%m %H:%M:%S.%f}</white>|"
                          "<level>{level}</level>|"
                          "<bold>{message}</bold>",
                   )
        return logger


with open("../config.toml", 'r') as file:
    conf = Configuration.model_validate(toml.load(file))

logger = LoguruConfiguration.get_logger("")  # noqa
