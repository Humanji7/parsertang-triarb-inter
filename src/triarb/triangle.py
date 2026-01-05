from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TriangleQuotes:
    a_usdt_ask: float
    a_b_bid: float
    b_usdt_bid: float


def compute_triangle_net_pct(
    quotes: TriangleQuotes,
    fee_pct_per_trade: float,
    slippage_pct_per_trade: float,
) -> float:
    if quotes.a_usdt_ask <= 0 or quotes.a_b_bid <= 0 or quotes.b_usdt_bid <= 0:
        raise ValueError("quotes must be positive")
    usdt_start = 1.0
    a_amount = usdt_start / quotes.a_usdt_ask
    b_amount = a_amount * quotes.a_b_bid
    usdt_end = b_amount * quotes.b_usdt_bid
    gross_pct = (usdt_end - usdt_start) * 100
    total_cost_pct = 3 * (fee_pct_per_trade + slippage_pct_per_trade)
    return gross_pct - total_cost_pct
