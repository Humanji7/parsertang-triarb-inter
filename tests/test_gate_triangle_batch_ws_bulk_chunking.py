import asyncio

from triarb.main import run_gate_triangle_batch_bridge_ws_bulk


def test_run_gate_triangle_batch_bridge_ws_bulk_chunks_calls():
    calls = []

    async def fake_multi(inst_ids, url="", timeout_s=0, allow_partial=False):
        calls.append(list(inst_ids))
        return {}

    async def run_test() -> None:
        await run_gate_triangle_batch_bridge_ws_bulk(
            assets=["ADA", "DOGE", "LTC", "ATOM", "DOT"],
            base="USDT",
            bridge="BTC",
            fee_pct_per_trade=0.1,
            slippage_pct_per_trade=0.05,
            min_net_pct=0.3,
            timeout_s=1.0,
            overall_timeout_s=1.0,
            chunk_size=2,
            fetch_gate_multi=fake_multi,
        )
        assert len(calls) == 3

    asyncio.run(run_test())
