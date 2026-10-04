"""Pricing for models newer than the ones upstream's tables know about.

Upstream `run_benchmark._RUN_PRICING` and `parse_logs._PRICING` stop at Sonnet 4.6 /
Opus 4.x and fall back to Sonnet 4.6 prices for anything else, which would misprice
every run below (and make the per-run budget kill fire at the wrong dollar amount).
USD per 1M tokens; cache_create is the 5-minute write (1.25x input). Source: Anthropic's
published API prices as of 2026-09.
"""

NEW_PRICING = [
    ("claude-sonnet-5",  {"input": 2.00,  "output": 10.00, "cache_create": 2.50,  "cache_read": 0.20}),
    ("claude-opus-5-5",  {"input": 4.00,  "output": 20.00, "cache_create": 5.00,  "cache_read": 0.20}),
    ("claude-fable-5-1", {"input": 10.00, "output": 50.00, "cache_create": 12.50, "cache_read": 0.25}),
]


def extend(table: list) -> None:
    """Prepend NEW_PRICING so the prefix match finds these before any fallback."""
    table[:0] = NEW_PRICING
