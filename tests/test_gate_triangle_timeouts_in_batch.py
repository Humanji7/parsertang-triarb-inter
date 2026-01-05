import asyncio

from triarb.gate_ws import BookTicker
from triarb.main import run_gate_triangle_batch_bridge


def test_run_gate_triangle_batch_bridge_skips_timeouts():
    async def fake_gate(inst_id: str, url: str = "") -> BookTicker:
        if inst_id.startswith("DOGE_"):
            raise TimeoutError("Gate timeout")
        return BookTicker(inst_id=inst_id, bid_px=6.0, ask_px=10.0, ts_ms=1)

    async def run_test() -> None:
        assets = ["ADA", "DOGE"]
        available = {"ADA_USDT", "DOGE_USDT", "ADA_BTC", "DOGE_BTC", "BTC_USDT"}
        rows = await run_gate_triangle_batch_bridge(
            assets=assets,
            base="USDT",
            bridge="BTC",
            fee_pct_per_trade=0.1,
            slippage_pct_per_trade=0.05,
            min_net_pct=0.3,
            available_pairs=available,
            max_triangles=None,
            fetch_gate=fake_gate,
        )
        assert len(rows) == 1

    asyncio.run(run_test())
