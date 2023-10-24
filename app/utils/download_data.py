import os
import zipfile
import urllib.request
import urllib.error

from app.configuration import logger
from app.schemas import path


class DataWorker:
    base_url: str = "https://data.binance.vision/data/futures/um/monthly/klines/"

    @classmethod
    def download_data(cls, symbol: str, timeframe: str, year: str, month: str):
        """
        :return: path to data or None if data not found or error.
        """
        try:
            file_name = f"{symbol.upper()}-{timeframe}-{year}-{month}"
            if cls._check_cached_data(file_name + ".csv"):
                logger.debug(f"Cached data for {file_name}")
                return os.path.join("..", "data", f"{file_name}.csv")
            postfix = f"{symbol.upper()}/{timeframe}/"
            cls._retrieve_data(file_name, postfix)
            return cls._extract_data(file_name)
        except urllib.error.HTTPError:
            logger.error(f"Data not found {file_name}.")
        except Exception as err:
            logger.error(f"Error while download data {file_name}: {err}")

    @classmethod
    def _check_cached_data(cls, file_name: str) -> bool:
        """
        Check cached data from 'data' folder
        :param file_name:
        :return:
        """
        downloaded_data = os.listdir("../data")
        if file_name in downloaded_data:
            return True
        return False

    @classmethod
    def _retrieve_data(cls, file_name: str, postfix: str) -> None:
        urllib.request.urlretrieve(
            cls.base_url + postfix + file_name + ".zip",
            os.path.join("..", "tmp", f"{file_name}.zip"))

    @classmethod
    def _extract_data(cls, file_name: str) -> path:
        with zipfile.ZipFile(os.path.join("..", "tmp", f"{file_name}.zip"), "r") as zip_ref:
            zip_ref.extract(f"{file_name}.csv", path=os.path.join("..", "data"))
        os.remove(os.path.join("..", "tmp", f"{file_name}.zip"))
        return os.path.join("..", "data", f"{file_name}.csv")
