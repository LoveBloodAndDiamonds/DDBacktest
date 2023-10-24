from app.schemas import Candle, path
from app.utils import DataWorker, parse_csv
from app.configuration import logger, conf


def main():
    data: list[Candle] = _collect_data()


def _collect_data() -> list[Candle]:
    extended_data = list()
    for year, month in _get_backtest_interval(
            start_year=conf.base.start_year,
            start_month=conf.base.strat_month,
            end_year=conf.base.end_year,
            end_month=conf.base.end_month):
        data: path = DataWorker.download_data(
            symbol=conf.base.symbol,
            timeframe=conf.base.interval,
            year=year,
            month=month)
        if data:
            data_csv: list[Candle] = parse_csv(data)
            extended_data.extend(data_csv)
            logger.debug(f"Data extended by: {data_csv[0].datetime} -> {data_csv[-1].datetime}")
        else:
            logger.error(f"No data for {year}-{month}")
            break
    logger.debug(f"""
        Collected big data:
        Start |    {str(extended_data[0].datetime)}
        End   |    {str(extended_data[-1].datetime)}
        Lenght|    {len(extended_data)}
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


if __name__ == '__main__':
    main()
