from datetime import timedelta

from tinkoff.invest import (
    AsyncClient,
    CandleInterval,
    Candle,
)
from tinkoff.invest.utils import now

from app.utils.config import config


async def get_monthly_hourly_candles(ticker: str) -> list[dict]:
    try:
        async with AsyncClient(config.tinkoff_api_token) as client:
            instruments = await client.instruments.shares()
            instrument = next((i for i in instruments.instruments if i.ticker == ticker), None)

            if not instrument:
                return []
            figi = instrument.figi
            to_date = now()
            from_date = to_date - timedelta(days=1)

            candles: list[Candle] = []
            try:
                async for candle in client.get_all_candles(
                        figi=figi,
                        from_=from_date,
                        to=to_date,
                        interval=CandleInterval.CANDLE_INTERVAL_HOUR,
                ):
                    candles.append(candle)
            except Exception as e:
                return []
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
    except Exception as e:
        return []
