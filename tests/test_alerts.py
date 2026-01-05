from triarb.alerts import format_signal


def test_alert_format():
    msg = format_signal("bybit", "okx", "USDT", "ADA", "DOT", "ARBITRUM", 1250, 0.42)
    assert "BYBIT → OKX" in msg
    assert "ΠNet" in msg
