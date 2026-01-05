from __future__ import annotations


def compute_spread_pct(buy_ask: float, sell_bid: float) -> float:
    if buy_ask <= 0:
        raise ValueError("buy_ask must be positive")
    return ((sell_bid - buy_ask) / buy_ask) * 100
