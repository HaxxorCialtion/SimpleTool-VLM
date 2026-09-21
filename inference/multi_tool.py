"""Host-side decoding for position-coded multi_tool ranking scores."""
from dataclasses import dataclass
import math

from .protocol import ProtocolError


@dataclass(frozen=True)
class MultiToolDecision:
    candidates: tuple[str, ...]
    scores: tuple[float, ...]
    selected: str


def decode(function, arguments, candidates, *, field_prefix="p"):
    """Map positional scores to candidates and select by argmax.

    Scores are bounded ranking values, not calibrated probabilities. No
    normalization or sum-to-one validation is performed.
    """
    candidates = tuple(candidates)
    if function != "multi_tool" or not 1 <= len(candidates) <= 6:
        raise ProtocolError("invalid multi_tool function or candidate count")
    expected = [f"{field_prefix}{i}" for i in range(1, len(candidates) + 1)]
    if set(arguments) != set(expected):
        raise ProtocolError("multi_tool fields do not match candidate count")
    scores = []
    for key in expected:
        value = arguments[key]
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
            raise ProtocolError(f"{key} must be a finite number")
        if not 0 <= value <= 1:
            raise ProtocolError(f"{key} must be between 0 and 1")
        scores.append(float(value))
    winner = max(range(len(scores)), key=scores.__getitem__)
    return MultiToolDecision(candidates, tuple(scores), candidates[winner])
