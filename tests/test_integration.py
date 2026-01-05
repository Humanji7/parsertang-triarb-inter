from triarb.main import run_mock_pipeline


def test_integration_signal_emitted():
    msg = run_mock_pipeline()
    assert msg is not None
    assert "BYBIT → OKX" in msg
