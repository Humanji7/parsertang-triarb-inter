from __future__ import annotations

from triarb.evaluator import compute_net_profit_pct


def should_signal(
    spread_pct: float,
    fee_pct: float,
    slippage_pct: float,
    min_net_pct: float,
) -> bool:
    net = compute_net_profit_pct(spread_pct, fee_pct, slippage_pct)
    return net >= min_net_pct
