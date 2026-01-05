import asyncio

from triarb.gate_ws import BookTicker
from triarb.main import run_okx_gate_spread_batch
from triarb.okx_ws import Ticker


def test_run_okx_gate_spread_batch_returns_rows():
    async def fake_okx(inst_id: str, url: str = "") -> Ticker:
        return Ticker(inst_id=inst_id, bid_px=99.0, ask_px=100.0, ts_ms=1)

    async def fake_gate(inst_id: str, url: str = "") -> BookTicker:
        return BookTicker(inst_id=inst_id, bid_px=101.0, ask_px=102.0, ts_ms=1)

    async def run_test() -> None:
        rows = await run_okx_gate_spread_batch(
            assets=["ADA", "DOGE"],
            base="USDT",
            fetch_okx=fake_okx,
            fetch_gate=fake_gate,
        )
        assert len(rows) == 2
        assert "spread_pct=1.0" in rows[0]

    asyncio.run(run_test())
