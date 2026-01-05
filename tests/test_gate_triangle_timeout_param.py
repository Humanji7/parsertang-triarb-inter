import asyncio

from triarb.gate_ws import BookTicker
from triarb.main import run_gate_triangle_filtered


def test_run_gate_triangle_filtered_passes_timeout():
    seen = {}

    async def fake_gate(inst_id: str, url: str = "", timeout_s: float | None = None) -> BookTicker:
        seen[inst_id] = timeout_s
        return BookTicker(inst_id=inst_id, bid_px=2.0, ask_px=2.1, ts_ms=1)

    async def run_test() -> None:
        await run_gate_triangle_filtered(
            a_asset="ADA",
            b_asset="DOGE",
            base="USDT",
            fee_pct_per_trade=0.1,
            slippage_pct_per_trade=0.05,
            min_net_pct=0.3,
            timeout_s=1.5,
            fetch_gate=fake_gate,
        )
        assert seen["ADA_USDT"] == 1.5
        assert seen["ADA_DOGE"] == 1.5
        assert seen["DOGE_USDT"] == 1.5

    asyncio.run(run_test())
