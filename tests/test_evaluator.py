from triarb.evaluator import compute_noptimal


def test_noptimal_respects_slippage_limit():
    orderbook_depth = [
        (1.00, 1000),
        (1.01, 1000),
    ]
    n = compute_noptimal(orderbook_depth, max_slip_pct=0.05)
    assert n > 0
