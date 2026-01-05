from triarb.evaluator import compute_noptimal


def test_noptimal_respects_slippage_limit():
    orderbook_depth = [
        (1.00, 1000),
        (1.01, 1000),
    ]
    n = compute_noptimal(orderbook_depth, max_slip_pct=0.05)
    assert n > 0
from triarb.evaluator import compute_net_profit_pct


def test_net_profit_pct():
    gross = 0.6
    fees = 0.2
    slip = 0.05
    assert compute_net_profit_pct(gross, fees, slip) == 0.35
