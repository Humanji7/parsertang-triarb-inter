import asyncio
import json

import pytest

from triarb.gate_ws import (
    build_gate_subscribe_message,
    fetch_one_gate_book_ticker,
    parse_gate_book_ticker_message,
)


def test_parse_gate_book_ticker_message():
    message = {
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
    ticker = parse_gate_book_ticker_message(message)
    assert ticker is not None
    assert ticker.inst_id == "BTC_USDT"
    assert ticker.bid_px == 19177.79
    assert ticker.ask_px == 19179.38
    assert ticker.ts_ms == 1606293275123


def test_build_gate_subscribe_message():
    message = build_gate_subscribe_message("BTC_USDT")
    assert message["channel"] == "spot.book_ticker"
    assert message["event"] == "subscribe"
    assert message["payload"] == ["BTC_USDT"]
    assert isinstance(message["time"], int)


def test_fetch_one_gate_book_ticker_from_local_server():
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
            ticker = await fetch_one_gate_book_ticker("BTC_USDT", url=url, timeout_s=2.0)
            assert ticker.bid_px == 19177.79
            assert ticker.ask_px == 19179.38

    asyncio.run(run_test())
