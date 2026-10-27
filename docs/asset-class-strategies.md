# Asset-class strategy notes (v0.47)

Research heuristics with multi-factor enhancements. Each class: edge hypothesis, entry, invalidation, horizon, size cap. Not a promise of returns.

Regime: trend (8-bar move >=2.5% , range under stress), range, stress (avg bar range >=3.5%).

Additional filters: MACD proxy (EMA12 > EMA26), RSI divergence (price higher high / RSI lower high = bearish, reverse for bullish), multi-TF consistency (short window aligns with longer), ADX-like (directional movement strength proxy via smoothed range).

## Major

Hypothesis: liquid majors trend with momentum confirmation. Entry: fast EMA > slow + MACD positive + RSI 40-70 + ADX strength + multi-TF align. Mean-reversion only in range with RSI <35 and bullish divergence. Cap 8%. Horizon 8/20 bars. Cost 8 bps.

## Large-cap alt

Hypothesis: volume-confirmed breakouts with momentum. Entry: close > prior 5-bar high, volume >1.2x, MACD positive, multi-TF, non-stress. Cap 4%. Cost 14 bps.

## Stablecoin

Hypothesis: peg integrity. Adaptive 15-50 bps watch/depeg alerts. No orders. Size zero.

## DeFi

Hypothesis: trend only in calm regimes. Entry: close > EMA8, realised vol <=5.5%, low anomaly, MACD positive, multi-TF. Cap 2%. Cost 22 bps.

## Meme

Hypothesis: rare qualified bursts. Entry: 12-18% 4-bar burst, rising volume, volume floor, extension <35% over 8, StochRSI not extreme, multi-TF consistency. Horizon 3 bars. Cap 0.5%. Cost 45 bps.

## L2

Hypothesis: relative strength vs benchmark. Entry: excess return >2.5% over 6 bars + MACD vs bench, benchmark non-stress. Cap 3%. Cost 16 bps.

## RWA

Hypothesis: slow assets. Entry: multi-scale trend (close > EMA + prior), gap <6-8% adaptive, low anomaly. Halt on stress/gap. Cap 2%, horizon 24. Cost 12 bps.

## Perpetual

Hypothesis: negative funding carry with contained drift. Entry: funding <= -4 bps, multi-period abs drift <3.5%, low anomaly, stability. Crowded funding (>=8 bps) alert. Cap 2%. Cost 10 bps. No liquidation modeling.

Out of scope: live routing, claims of future returns.
