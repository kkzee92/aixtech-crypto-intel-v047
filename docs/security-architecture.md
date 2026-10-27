# Security architecture (v0.47)

Research control plane. Not a certified product or legal advice.

## Trust boundaries

Synthetic/public data -> source attestation + lineage seal -> strategy + regime/anomaly -> multi-gate risk (incl. correlation) -> paper fill -> hash-chained audit.

No order router. assert_paper_only refuses non-PAPER. refuse_trade_secret rejects credential-like names. No role enables live.

## Roles

Researcher / Auditor / Operator: scan, audit, kill switch. Denied: place order, withdraw, enable live. No trader role.

## Data classes and handling

Public market data: synthetic. Secrets: never stored. Wallet/seed/private key: redacted and banned from fixtures. Personal data: PDPA tripwire.

Expanded redaction: BIP39 seed words sequences, WIF/private key patterns, PEM blocks, high-entropy hex/base58, ETH 0x64, etc. Shannon entropy proxy for anomaly.

## Lineage and integrity

attest_source: hash(label + body). Sealed multi-hash: SHA-256(source_hash + timestamp + optional code digest). Merkle-style chaining for multi-events. Feed status: non-positive, stale (>15min), jump >25%.

## Threats and controls

Secret committed: gitleaks + expanded redaction. Trade key: refuse. Fixture injection: SYNTHETIC required + attestation. Stale/jump: feed status. Oversized risk: class caps + confidence + correlation + anomaly. Audit tamper: SHA-256 chain + seals. Live mistake: mode guard + RBAC. Privilege creep: no order role.

## Incident handling

1. Kill switch. 2. Freeze audit + record seals. 3. Rotate external secrets if pasted. 4. No public issue with secrets. 5. Human review.

Operating rules: read-only market creds separate; logs redacted; research default; broker promotion separate human-approved system.
