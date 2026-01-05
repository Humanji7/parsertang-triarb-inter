import asyncio

from triarb.gate_ws import BookTicker
from triarb.main import run_gate_triangle_filtered


def test_run_gate_triangle_filtered_calls_on_error():
    seen: list[str] = []

    async def fake_gate(inst_id: str, url: str = "", timeout_s: float | None = None) -> BookTicker:
        if inst_id == "ADA_DOGE":
            raise TimeoutError("Gate timeout")
        return BookTicker(inst_id=inst_id, bid_px=2.0, ask_px=2.1, ts_ms=1)

    def on_error(inst_id: str, exc: Exception) -> None:
        seen.append(inst_id)

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
            on_error=on_error,
        )
        assert "ADA_DOGE" in seen

    asyncio.run(run_test())
