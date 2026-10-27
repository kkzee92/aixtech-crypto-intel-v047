"""Cyber and data-security controls (enhanced v0.47)."""

from __future__ import annotations

import hashlib
import math
import re
from dataclasses import dataclass
from datetime import datetime, timezone

from crypto_intel.models import AuditEvent, ExecutionMode

SECRET_PATTERNS = (
    re.compile(r"(?i)(api[_-]?key|secret|password|token|private[_-]?key)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{12,}"),
    re.compile(r"\b(?:sk|pk)_(?:live|test)_[A-Za-z0-9]{8,}\b"),
    re.compile(r"\b[A-Z0-9._%+\-]+@[A-Z0-9.\-]+\.[A-Z]{2,}\b", re.IGNORECASE),
    re.compile(r"\b(?:5[HJK][1-9A-HJ-NP-Za-km-z]{49,50}|K[1-9A-HJ-NP-Za-km-z]{51}|L[1-9A-HJ-NP-Za-km-z]{51})\b"),  # WIF-like
    re.compile(r"\b0x[a-fA-F0-9]{64}\b"),  # ETH private key style
    re.compile(r"-----BEGIN (?:RSA |EC )?PRIVATE KEY-----"),
)

WALLET_PATTERN = re.compile(r"\b0x[a-fA-F0-9]{40}\b")
SEED_PATTERN = re.compile(r"(?i)\b(?:abandon|ability|able|about|above|absent|absorb|abstract|absurd|abuse)\b(?:\s+\w+){11,23}\b")  # BIP39 proxy


@dataclass(frozen=True)
class DataClassification:
    field: str
    level: str
    retention: str


CLASSIFICATION = (
    DataClassification("symbol", "public", "research"),
    DataClassification("ohlcv", "public-market", "research"),
    DataClassification("exchange_api_key", "secret", "never stored"),
    DataClassification("wallet_address", "sensitive-identifier", "do not fixture"),
    DataClassification("seed_phrase", "secret", "never store"),
    DataClassification("private_key", "secret", "never store"),
)


def shannon_entropy(text: str) -> float:
    if not text:
        return 0.0
    freq = {}
    for c in text:
        freq[c] = freq.get(c, 0) + 1
    length = len(text)
    return -sum((count / length) * math.log2(count / length) for count in freq.values())


def redact(text: str) -> str:
    cleaned = text
    for pattern in SECRET_PATTERNS:
        cleaned = pattern.sub("[REDACTED]", cleaned)
    cleaned = WALLET_PATTERN.sub("[WALLET]", cleaned)
    cleaned = SEED_PATTERN.sub("[SEED_REDACTED]", cleaned)
    # High-entropy heuristic
    if shannon_entropy(cleaned) > 4.5 and len(cleaned) > 20:
        cleaned = "[HIGH_ENTROPY_REDACTED]"
    return cleaned


def contains_secret(text: str) -> bool:
    return any(pattern.search(text) for pattern in SECRET_PATTERNS) or bool(WALLET_PATTERN.search(text)) or bool(SEED_PATTERN.search(text))


def assert_paper_only(mode: ExecutionMode) -> None:
    if mode is not ExecutionMode.PAPER:
        raise PermissionError("live execution is disabled; this system is paper-only")


def hash_event(previous_hash: str, sequence: int, action: str, detail: str) -> str:
    material = f"{previous_hash}|{sequence}|{action}|{detail}".encode()
    return hashlib.sha256(material).hexdigest()


def seal_lineage(source_hash: str, extra: str = "") -> str:
    ts = datetime.now(timezone.utc).isoformat()
    material = f"{source_hash}|{ts}|{extra}".encode()
    return hashlib.sha256(material).hexdigest()


class AuditLog:
    """Append-only hash chain with lineage seals."""

    def __init__(self) -> None:
        self.events: list[AuditEvent] = []
        self._previous = "GENESIS"

    def append(self, action: str, detail: str, source_hash: str = "") -> AuditEvent:
        safe_detail = redact(detail)
        sequence = len(self.events) + 1
        digest = hash_event(self._previous, sequence, action, safe_detail)
        seal = seal_lineage(source_hash or digest, action) if source_hash or True else ""
        event = AuditEvent(sequence, action, safe_detail, self._previous, digest, seal)
        self.events.append(event)
        self._previous = digest
        return event

    def verify(self) -> bool:
        previous = "GENESIS"
        for event in self.events:
            expected = hash_event(previous, event.sequence, event.action, event.detail)
            if event.previous_hash != previous or event.digest != expected:
                return False
            previous = event.digest
        return True
