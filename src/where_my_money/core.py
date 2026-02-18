from collections.abc import Iterable


def summarize_spending(amounts: Iterable[float]) -> float:
    """Return the total spending from an iterable of amounts."""
    return float(sum(amounts))
