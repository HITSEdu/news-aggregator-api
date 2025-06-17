import asyncio
from datetime import datetime, timedelta
from tinkoff.invest import (
    AsyncClient,
    CandleInterval,
    Candle,
)
from tinkoff.invest.utils import now

API_TOKEN = "t.4_kNUKFVaFH2hVUcTlIOUUD2KT7BujUAbA1B-gm4TRInfUd9v_e6uWCPu8YgXdhUnEMLCkmZk0_HLa9vlfCNEQ"  # Замените на ваш токен Tinkoff Invest API
TICKER = "SBER"  # Тикер акции (SBER, GAZP, VTBR и т.д.)


async def get_instrument_figi(client: AsyncClient, ticker: str) -> str:
    """Получаем FIGI инструмента по тикеру"""
    instruments = await client.instruments.shares()
    instrument = next(i for i in instruments.instruments if i.ticker == ticker)
    return instrument.figi


async def get_monthly_hourly_candles(ticker: str) -> list[dict]:
    """Получаем часовые свечи за последний месяц"""
    async with AsyncClient(API_TOKEN) as client:
        # 1. Получаем FIGI инструмента
        figi = await get_instrument_figi(client, ticker)

        # 2. Определяем даты (сегодня и месяц назад)
        to_date = now()
        from_date = to_date - timedelta(days=30)

        # 3. Запрашиваем свечи с часовым интервалом
        candles: list[Candle] = []
        async for candle in client.get_all_candles(
            figi=figi,
            from_=from_date,
            to=to_date,
            interval=CandleInterval.CANDLE_INTERVAL_HOUR,
        ):
            candles.append(candle)

        # 4. Обрабатываем полученные свечи
        return [
            {
                "time": candle.time,
                "open": candle.open.units + candle.open.nano / 1e9,
                "close": candle.close.units + candle.close.nano / 1e9,
                "high": candle.high.units + candle.high.nano / 1e9,
                "low": candle.low.units + candle.low.nano / 1e9,
                "volume": candle.volume,
            }
            for candle in candles
        ]
