from triarb.spread import compute_spread_pct


def test_compute_spread_pct_positive():
    pct = compute_spread_pct(buy_ask=100.0, sell_bid=101.0)
    assert round(pct, 4) == 1.0


def test_compute_spread_pct_zero():
    pct = compute_spread_pct(buy_ask=100.0, sell_bid=100.0)
    assert pct == 0.0


def test_compute_spread_pct_negative():
    pct = compute_spread_pct(buy_ask=101.0, sell_bid=100.0)
    assert round(pct, 4) == -0.9901
