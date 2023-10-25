import pandas as pd
import warnings

from app.backtest import Backtest
from app.configuration import logger, conf
from app.strategies.macd_strategy import MACDStrategy
from app.utils import DataWorker


def main():
    data: pd.DataFrame = _collect_data()
    if _check_dataframe_integrity(data):
        logger.success("Dataframe monotonic_increasing and unique indexing!")
        backtest = Backtest(data=data, strategy=MACDStrategy)
        backtest.run()
    else:
        logger.error("Dataframe with errors")


def _collect_data() -> pd.DataFrame:
    extended_data = pd.DataFrame(columns=['datetime', 'open', 'high', 'low', 'close'])

    for year, month in _get_backtest_interval(
            start_year=conf.backtest_ranges.start_year,
            start_month=conf.backtest_ranges.strat_month,
            end_year=conf.backtest_ranges.end_year,
            end_month=conf.backtest_ranges.end_month):
        data: str = DataWorker.download_data(
            symbol=conf.base_conf.symbol,
            timeframe=conf.base_conf.interval,
            year=year,
            month=month)
        if data:
            data_csv: pd.DataFrame = pd.read_csv(data)
            data_csv['datetime'] = pd.to_datetime(data_csv['open_time'], unit='ms')
            data_csv.dropna()
            data_csv = data_csv.drop(['quote_volume', 'count', 'taker_buy_volume', 'taker_buy_quote_volume',
                                      'ignore', 'volume', 'open_time', 'close_time'], axis=1)
            extended_data = pd.concat([extended_data, data_csv], ignore_index=True, join='outer')
            logger.debug(f"Data extended by: {data_csv.iloc[0]['datetime']} -> {data_csv.iloc[-1]['datetime']}")
        else:
            logger.error(f"No data for {year}-{month}")
            break
    logger.debug(f"""
        Collected big data:
        Start |    {str(extended_data.iloc[0]['datetime'])}
        End   |    {str(extended_data.iloc[-1]['datetime'])}
        Length|    {len(extended_data)}
        """)

    return extended_data


def _get_backtest_interval(start_year, start_month, end_year, end_month) -> list[list[str]]:
    # Создаем список всех месяцев в заданном временном интервале
    months = []
    for year in range(start_year, end_year + 1):
        # Устанавливаем начальный и конечный месяц для текущего года
        start = start_month if year == start_year else 1
        end = end_month if year == end_year else 12
        # Добавляем все месяцы в текущем году в список
        for month in range(start, end + 1):
            month = f"0{month}" if len(str(month)) == 1 else str(month)
            months.append([str(year), month])

    return months


def _check_dataframe_integrity(df: pd.DataFrame) -> bool:
    result = list()

    # Проверка индексов
    if df.index.is_unique and df.index.is_monotonic_increasing:
        result.append(True)
    else:
        result.append(False)

    # Проверка столбца "datetime"
    if pd.api.types.is_datetime64_any_dtype(df['datetime']):
        if df['datetime'].is_monotonic_increasing:
            result.append(True)
        else:
            result.append(False)
    else:
        result.append(False)

    return all(result)


if __name__ == '__main__':
    warnings.simplefilter(action='ignore', category=FutureWarning)
    main()
