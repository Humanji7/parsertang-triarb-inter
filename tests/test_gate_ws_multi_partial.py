import asyncio
import json

import pytest

from triarb.gate_ws import fetch_gate_book_tickers


def test_fetch_gate_book_tickers_allows_partial_on_timeout():
    async def run_test() -> None:
        websockets = pytest.importorskip("websockets")

        messages = [
            {
                "time": 1606293275,
                "time_ms": 1606293275723,
                "channel": "spot.book_ticker",
                "event": "update",
                "result": {"t": 1606293275123, "u": 1, "s": "ADA_USDT", "b": "1", "B": "1", "a": "1.1", "A": "1"},
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
            tickers = await fetch_gate_book_tickers(
                ["ADA_USDT", "ADA_BTC"],
                url=url,
                timeout_s=0.5,
                allow_partial=True,
            )
            assert set(tickers.keys()) == {"ADA_USDT"}

    asyncio.run(run_test())
