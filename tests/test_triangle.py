from triarb.triangle import TriangleQuotes, compute_triangle_net_pct


def test_compute_triangle_net_pct_positive():
    quotes = TriangleQuotes(
        a_usdt_ask=10.0,
        a_b_bid=2.0,
        b_usdt_bid=6.0,
    )
    net = compute_triangle_net_pct(quotes, fee_pct_per_trade=0.1, slippage_pct_per_trade=0.05)
    # 1 USDT -> 0.1 A -> 0.2 B -> 1.2 USDT = 20% gross, net -0.45% fees/slip = 19.55
    assert round(net, 2) == 19.55


def test_compute_triangle_net_pct_negative():
    quotes = TriangleQuotes(
        a_usdt_ask=10.0,
        a_b_bid=1.0,
        b_usdt_bid=9.0,
    )
    net = compute_triangle_net_pct(quotes, fee_pct_per_trade=0.1, slippage_pct_per_trade=0.05)
    assert net < 0
