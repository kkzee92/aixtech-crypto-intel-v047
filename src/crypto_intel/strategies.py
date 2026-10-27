"""Asset-class strategy research rules (enhanced v0.47).

Transparent multi-factor heuristics. Not forecasts.
"""

from __future__ import annotations

from statistics import fmean

from crypto_intel.models import AssetClass, Candle, Side, Signal
from crypto_intel.regime import Regime, classify  # assume regime.py exists or stub


def _ema(values: list[float], span: int) -> float:
    if not values:
        return 0.0
    alpha = 2.0 / (span + 1)
    value = values[0]
    for point in values[1:]:
        value = alpha * point + (1 - alpha) * value
    return value


def _macd_proxy(closes: list[float]) -> float:
    if len(closes) < 26:
        return 0.0
    return _ema(closes, 12) - _ema(closes, 26)


def _rsi(closes: list[float], period: int = 14) -> float:
    if len(closes) < period + 1:
        return 50.0
    changes = [closes[i] / closes[i - 1] - 1.0 for i in range(1, len(closes))]
    gains = [max(c, 0.0) for c in changes[-period:]]
    losses = [abs(min(c, 0.0)) for c in changes[-period:]]
    avg_loss = fmean(losses) if losses else 0.0
    if avg_loss == 0:
        return 100.0
    rs = fmean(gains) / avg_loss
    return 100.0 - (100.0 / (1.0 + rs))


def _adx_proxy(candles: list[Candle]) -> float:
    # Simplified directional strength
    if len(candles) < 5:
        return 0.0
    ranges = [(c.high - c.low) / c.close for c in candles[-5:]]
    return fmean(ranges) * 100 if ranges else 0.0


def signal_for(candles: list[Candle], benchmark: list[Candle] | None = None) -> Signal:
    if len(candles) < 8:
        raise ValueError("need at least 8 candles")
    asset_class = candles[-1].asset_class
    closes = [c.close for c in candles]
    regime = Regime.TREND  # stub; integrate real classify
    macd = _macd_proxy(closes)
    rsi = _rsi(closes)
    adx = _adx_proxy(candles)
    # Placeholder multi-factor logic; expand per class as in docs
    if asset_class is AssetClass.MAJOR and macd > 0 and 40 <= rsi <= 70 and adx > 1.5:
        return Signal(candles[-1].symbol, asset_class, Side.LONG, 0.72, "major multi-factor: MACD+RSI+ADX", 0.02, 0.06, 20)
    # ... extend for other classes similarly
    return Signal(candles[-1].symbol, asset_class, Side.FLAT, 0.4, "no edge in enhanced rules", 0.01, 0.0, 1)
