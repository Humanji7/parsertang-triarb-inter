from triarb.triangle_candidates import build_gate_triangle_candidates_with_bridge


def test_build_gate_triangle_candidates_with_bridge():
    assets = ["ADA", "DOGE", "LTC"]
    available = {"ADA_USDT", "DOGE_USDT", "LTC_USDT", "ADA_BTC", "DOGE_BTC", "BTC_USDT"}
    candidates = build_gate_triangle_candidates_with_bridge(
        assets=assets,
        base="USDT",
        bridge="BTC",
        available_pairs=available,
    )
    assert ("ADA", "BTC") in candidates
    assert ("DOGE", "BTC") in candidates
