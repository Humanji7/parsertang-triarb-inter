import asyncio

from triarb.gate_ws import BookTicker
from triarb.main import run_gate_triangle_batch_bridge


def test_run_gate_triangle_batch_bridge_uses_concurrency_limit():
    active = 0
    peak = 0

    async def fake_gate(inst_id: str, url: str = "", timeout_s: float | None = None) -> BookTicker:
        nonlocal active, peak
        active += 1
        peak = max(peak, active)
        await asyncio.sleep(0)
        active -= 1
        return BookTicker(inst_id=inst_id, bid_px=6.0, ask_px=10.0, ts_ms=1)

    async def run_test() -> None:
        assets = ["ADA", "DOGE", "LTC", "ATOM"]
        available = {"ADA_USDT", "DOGE_USDT", "LTC_USDT", "ATOM_USDT", "ADA_BTC", "DOGE_BTC", "LTC_BTC", "ATOM_BTC", "BTC_USDT"}
        await run_gate_triangle_batch_bridge(
            assets=assets,
            base="USDT",
            bridge="BTC",
            fee_pct_per_trade=0.1,
            slippage_pct_per_trade=0.05,
            min_net_pct=0.3,
            available_pairs=available,
            concurrency_limit=2,
            fetch_gate=fake_gate,
        )
        assert peak <= 2

    asyncio.run(run_test())
