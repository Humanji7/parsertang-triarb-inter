import asyncio

from triarb.main import run_gate_triangle_batch_bridge_ws_bulk


def test_run_gate_triangle_batch_bridge_ws_bulk_enforces_overall_timeout():
    async def fake_multi(inst_ids, url="", timeout_s=0, allow_partial=False):
        await asyncio.sleep(0.2)
        return {}

    async def run_test() -> None:
        rows = await run_gate_triangle_batch_bridge_ws_bulk(
            assets=["ADA"],
            base="USDT",
            bridge="BTC",
            fee_pct_per_trade=0.1,
            slippage_pct_per_trade=0.05,
            min_net_pct=0.3,
            timeout_s=0.01,
            overall_timeout_s=0.01,
            fetch_gate_multi=fake_multi,
        )
        assert rows == []

    asyncio.run(run_test())
