import asyncio

from triarb.gate_ws import BookTicker
from triarb.main import run_gate_triangle_filtered


def test_run_gate_triangle_filtered_returns_only_meeting_threshold():
    async def fake_gate(inst_id: str, url: str = "") -> BookTicker:
        if inst_id == "ADA_USDT":
            return BookTicker(inst_id=inst_id, bid_px=9.5, ask_px=10.0, ts_ms=1)
        if inst_id == "ADA_DOGE":
            return BookTicker(inst_id=inst_id, bid_px=2.0, ask_px=2.1, ts_ms=1)
        if inst_id == "DOGE_USDT":
            return BookTicker(inst_id=inst_id, bid_px=6.0, ask_px=6.1, ts_ms=1)
        raise ValueError("unexpected inst_id")

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
        assert len(rows) == 1
        assert "net_pct=19.55" in rows[0]

    asyncio.run(run_test())
