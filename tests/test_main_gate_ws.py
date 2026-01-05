import asyncio
import json

import pytest

from triarb.main import run_gate_ws_sample


def test_run_gate_ws_sample_from_local_server():
    async def run_test() -> None:
        websockets = pytest.importorskip("websockets")

        book_ticker_message = {
            "time": 1606293275,
            "time_ms": 1606293275723,
            "channel": "spot.book_ticker",
            "event": "update",
            "result": {
                "t": 1606293275123,
                "u": 48733182,
                "s": "BTC_USDT",
                "b": "19177.79",
                "B": "0.0003341504",
                "a": "19179.38",
                "A": "0.09",
            },
        }

        async def handler(websocket):
            await websocket.recv()
            await websocket.send(json.dumps({"event": "subscribe", "channel": "spot.book_ticker"}))
            await websocket.send(json.dumps(book_ticker_message))

        async with websockets.serve(handler, "localhost", 0) as server:
            port = server.sockets[0].getsockname()[1]
            url = f"ws://localhost:{port}"
            text = await run_gate_ws_sample("BTC_USDT", url=url)
            assert "BTC_USDT" in text
            assert "19177.79" in text
            assert "19179.38" in text

    asyncio.run(run_test())
