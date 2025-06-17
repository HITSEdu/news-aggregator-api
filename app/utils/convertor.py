from typing import List


def ticker_db_to_dto(tickers_string: str) -> List[str]:
    return tickers_string.split(";")


def ticker_dto_to_dbo(tickers_list: List[str]) -> str:
    return ';'.join(tickers_list)
