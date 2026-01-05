import asyncio

from triarb.gate_ws import BookTicker
from triarb.main import run_okx_gate_spread_filtered
from triarb.okx_ws import Ticker


def test_run_okx_gate_spread_filtered_only_returns_meeting_threshold():
    async def fake_okx(inst_id: str, url: str = "") -> Ticker:
        return Ticker(inst_id=inst_id, bid_px=99.0, ask_px=100.0, ts_ms=1)

    async def fake_gate(inst_id: str, url: str = "") -> BookTicker:
        return BookTicker(inst_id=inst_id, bid_px=101.0, ask_px=102.0, ts_ms=1)

    async def run_test() -> None:
        rows = await run_okx_gate_spread_filtered(
            assets=["ADA", "DOGE"],
            base="USDT",
            fee_pct=0.2,
            slippage_pct=0.1,
            min_net_pct=0.3,
            fetch_okx=fake_okx,
            fetch_gate=fake_gate,
        )
        assert len(rows) == 2
        assert "net_pct=0.7" in rows[0]

    asyncio.run(run_test())
