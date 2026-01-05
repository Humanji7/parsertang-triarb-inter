from triarb.triangle_candidates import build_gate_triangle_candidates


def test_build_gate_triangle_candidates_filters_missing_pairs():
    assets = ["ADA", "DOGE", "LTC"]
    available = {"ADA_USDT", "DOGE_USDT", "ADA_DOGE"}
    candidates = build_gate_triangle_candidates(assets, base="USDT", available_pairs=available)
    assert candidates == [("ADA", "DOGE")]
