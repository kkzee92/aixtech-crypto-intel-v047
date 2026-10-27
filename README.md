# AIxTech crypto intel v0.47: paper-only trading information system

Research harness for automated cryptocurrency **information** and paper strategy
evaluation. It does not place live orders, does not store exchange secrets, and
is not financial advice.

Builds on [zeekiankok92/aixtech-crypto-intel](https://github.com/zeekiankok92/aixtech-crypto-intel) (v0.2) and successive enhancements under kkzee92.

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![version](https://img.shields.io/badge/version-0.47.0-blue)
![mode](https://img.shields.io/badge/execution-paper%20only-orange)
![Licence](https://img.shields.io/badge/licence-MIT-green)

## Enhancements in v0.47

- Multi-factor strategies: MACD proxy (fast/slow EMA crossover), RSI divergence detection, multi-timeframe consistency (short vs longer window), ADX-like trend strength filter.
- Adaptive position sizing reduced under high volatility or anomaly scores.
- Portfolio-level correlation risk gate: refuse or shrink if pairwise correlation exceeds threshold across active signals.
- Strengthened zero-trust security: expanded redaction for BIP39 seed phrases, private key patterns (WIF, hex, PEM), high-entropy strings; sealed multi-hash lineage (source + timestamp + code hash); entropy anomaly scoring.
- Updated playbooks and risk thresholds per asset class.
- Research only; synthetic fixtures recommended.

See [docs/asset-class-strategies.md](docs/asset-class-strategies.md) and [docs/security-architecture.md](docs/security-architecture.md).

## What it does

- Classifies into eight asset classes with enhanced multi-factor research rules.
- Labels regime (trend/range/stress) + volatility tier + anomaly.
- Scores signal then multi-gate risk (class caps, confidence, correlation, anomaly).
- Paper fills with class costs; hash-chained audit with lineage seals.
- No live execution, no secret storage.

| Asset class | Enhanced research rule | Risk cap | Cost |
|---|---|---|---|
| Major | Multi-EMA + MACD + RSI div + ADX strength; range reversion only | 8% | 8 bps |
| Large-cap alt | Volume breakout + MACD confirm + multi-TF | 4% | 14 bps |
| Stablecoin | Peg deviation alerts only (adaptive bands) | 0% | n/a |
| DeFi | Calm multi-scale trend + low anomaly | 2% | 22 bps |
| Meme | Qualified burst + StochRSI + consistency + hard horizon | 0.5% | 45 bps |
| L2 | Relative strength + MACD vs benchmark | 3% | 16 bps |
| RWA | Slow multi-scale + gap/anomaly halt | 2% | 12 bps |
| Perpetual | Negative funding carry with contained multi-period drift + low anomaly | 2% | 10 bps |

## Run

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
PYTHONPATH=src python -m crypto_intel scan fixtures/candles_synthetic.json
PYTHONPATH=src pytest tests/ -q
```

Generate fixtures with scripts/make_fixtures.py (synthetic only).

## Controls

Paper-only mode guard. No trade keys. Class caps, confidence floors, kill switch, drawdown, correlation, anomaly gates. Hash-chained audit + sealed lineage. Expanded redaction. PDPA tripwire. gitleaks recommended in CI.

## Honesty

No live connector included. Strategy scores describe synthetic data. Not financial, legal, or compliance advice. Research only.
