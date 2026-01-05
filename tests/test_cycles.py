from triarb.cycles import build_cycles


def test_build_cycles_base_to_base():
    coins = ["ADA", "DOT", "AVAX"]
    cycles = build_cycles(coins, base="USDT")
    assert ("USDT", "ADA", "DOT", "USDT") in cycles
    assert ("USDT", "DOT", "ADA", "USDT") in cycles
