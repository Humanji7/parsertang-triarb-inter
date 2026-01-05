from triarb.config import Settings


def test_settings_defaults():
    s = Settings()
    assert s.exchanges == ["bybit", "okx"]
    assert s.base_asset == "USDT"
    assert s.min_net_profit == 0.3
