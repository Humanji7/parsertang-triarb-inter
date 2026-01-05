import asyncio
import json

import pytest

from triarb.gate_ws import fetch_gate_book_tickers


def test_fetch_gate_book_tickers_from_local_server():
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
                "result": {"t": 1606293275123, "u": 3, "s": "BTC_USDT", "b": "3", "B": "1", "a": "3.1", "A": "1"},
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
            tickers = await fetch_gate_book_tickers(["ADA_USDT", "ADA_BTC", "BTC_USDT"], url=url, timeout_s=2.0)
            assert set(tickers.keys()) == {"ADA_USDT", "ADA_BTC", "BTC_USDT"}
            assert tickers["ADA_BTC"].bid_px == 2.0

    asyncio.run(run_test())
