import asyncio
import json

import pytest

from triarb.main import run_gate_triangle_batch_bridge_ws_bulk


def test_run_gate_triangle_batch_bridge_ws_bulk_from_local_server():
    async def run_test() -> None:
        websockets = pytest.importorskip("websockets")

        messages = [
            {
                "time": 1606293275,
                "time_ms": 1606293275723,
                "channel": "spot.book_ticker",
                "event": "update",
                "result": {"t": 1606293275123, "u": 1, "s": "ADA_USDT", "b": "9.5", "B": "1", "a": "10", "A": "1"},
            },
            {
                "time": 1606293275,
                "time_ms": 1606293275723,
                "channel": "spot.book_ticker",
                "event": "update",
                "result": {"t": 1606293275123, "u": 2, "s": "ADA_BTC", "b": "2", "B": "1", "a": "2.1", "A": "1"},
            },
            {
                "time": 1606293275,
                "time_ms": 1606293275723,
                "channel": "spot.book_ticker",
                "event": "update",
                "result": {"t": 1606293275123, "u": 3, "s": "BTC_USDT", "b": "6", "B": "1", "a": "6.1", "A": "1"},
            },
        ]

        async def handler(websocket):
            await websocket.recv()
            await websocket.send(json.dumps({"event": "subscribe", "channel": "spot.book_ticker"}))
            for msg in messages:
                await websocket.send(json.dumps(msg))

        async with websockets.serve(handler, "localhost", 0) as server:
            port = server.sockets[0].getsockname()[1]
            url = f"ws://localhost:{port}"
            rows = await run_gate_triangle_batch_bridge_ws_bulk(
                assets=["ADA"],
                base="USDT",
                bridge="BTC",
                fee_pct_per_trade=0.1,
                slippage_pct_per_trade=0.05,
                min_net_pct=0.3,
                gate_url=url,
                timeout_s=2.0,
            )
            assert len(rows) == 1
            assert "ADA->BTC->USDT" in rows[0]

    asyncio.run(run_test())
