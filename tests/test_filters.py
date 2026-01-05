import asyncio

from triarb.filters import should_signal


def test_should_signal_true_when_net_meets_threshold():
    assert should_signal(spread_pct=0.6, fee_pct=0.2, slippage_pct=0.1, min_net_pct=0.3)


def test_should_signal_false_when_net_below_threshold():
    assert not should_signal(spread_pct=0.4, fee_pct=0.2, slippage_pct=0.1, min_net_pct=0.3)


def test_should_signal_false_when_negative_net():
    assert not should_signal(spread_pct=0.1, fee_pct=0.2, slippage_pct=0.1, min_net_pct=0.3)
