from __future__ import annotations

from triarb.alerts import format_signal
from triarb.evaluator import compute_net_profit_pct, compute_noptimal
from triarb.feeder import mock_orderbook_depth


def run_mock_pipeline() -> str | None:
    depth = mock_orderbook_depth()
    n_opt = compute_noptimal(depth, max_slip_pct=0.05)
    if n_opt <= 0:
        return None
    gross = 0.6
    fees = 0.2
    slip = 0.05
    net = compute_net_profit_pct(gross, fees, slip)
    if net <= 0.3:
        return None
    return format_signal("bybit", "okx", "USDT", "ADA", "DOT", "ARBITRUM", n_opt, net)
