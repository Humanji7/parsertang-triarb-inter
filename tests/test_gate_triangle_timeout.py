import asyncio

from triarb.gate_ws import BookTicker
from triarb.main import run_gate_triangle_filtered


def test_run_gate_triangle_filtered_skips_timeouts():
    async def fake_gate(inst_id: str, url: str = "") -> BookTicker:
        if inst_id == "ADA_DOGE":
            raise TimeoutError("Gate timeout")
        return BookTicker(inst_id=inst_id, bid_px=2.0, ask_px=2.1, ts_ms=1)

    async def run_test() -> None:
        rows = await run_gate_triangle_filtered(
            a_asset="ADA",
            b_asset="DOGE",
            base="USDT",
            fee_pct_per_trade=0.1,
            slippage_pct_per_trade=0.05,
            min_net_pct=0.3,
            fetch_gate=fake_gate,
        )
        assert rows == []

    asyncio.run(run_test())
