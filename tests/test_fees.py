from triarb.fees import FeeCache


def test_fee_cache_set_get():
    cache = FeeCache()
    cache.set_trade_fee("bybit", 0.1)
    assert cache.get_trade_fee("bybit") == 0.1
