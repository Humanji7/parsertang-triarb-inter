import asyncio
import json

import pytest

from triarb.okx_ws import build_okx_subscribe_message, fetch_one_okx_ticker, parse_okx_ticker_message


def test_parse_okx_ticker_message():
    message = {
        "arg": {"channel": "tickers", "instId": "BTC-USDT"},
        "data": [
            {
                "instType": "SPOT",
                "instId": "BTC-USDT",
                "last": "9999.99",
                "lastSz": "0.1",
                "askPx": "9999.99",
                "askSz": "11",
                "bidPx": "8888.88",
                "bidSz": "5",
                "open24h": "9000",
                "high24h": "10000",
                "low24h": "8888.88",
                "volCcy24h": "2222",
                "vol24h": "2222",
                "sodUtc0": "2222",
                "sodUtc8": "2222",
                "ts": "1597026383085",
            }
        ],
    }
    ticker = parse_okx_ticker_message(message)
    assert ticker is not None
    assert ticker.inst_id == "BTC-USDT"
    assert ticker.bid_px == 8888.88
    assert ticker.ask_px == 9999.99
    assert ticker.ts_ms == 1597026383085


def test_build_okx_subscribe_message():
    message = build_okx_subscribe_message("BTC-USDT")
    assert message["op"] == "subscribe"
    assert message["args"][0]["channel"] == "tickers"
    assert message["args"][0]["instId"] == "BTC-USDT"


def test_fetch_one_okx_ticker_from_local_server():
    async def run_test() -> None:
        websockets = pytest.importorskip("websockets")

        ticker_message = {
            "arg": {"channel": "tickers", "instId": "BTC-USDT"},
            "data": [
                {
                    "instType": "SPOT",
                    "instId": "BTC-USDT",
                    "last": "9999.99",
                    "lastSz": "0.1",
                    "askPx": "9999.99",
                    "askSz": "11",
                    "bidPx": "8888.88",
                    "bidSz": "5",
                    "open24h": "9000",
                    "high24h": "10000",
                    "low24h": "8888.88",
                    "volCcy24h": "2222",
                    "vol24h": "2222",
                    "sodUtc0": "2222",
                    "sodUtc8": "2222",
                    "ts": "1597026383085",
                }
            ],
        }

        async def handler(websocket):
            await websocket.recv()
            await websocket.send(
                json.dumps({"event": "subscribe", "arg": {"channel": "tickers", "instId": "BTC-USDT"}})
            )
            await websocket.send(json.dumps(ticker_message))

        async with websockets.serve(handler, "localhost", 0) as server:
            port = server.sockets[0].getsockname()[1]
            url = f"ws://localhost:{port}"
            ticker = await fetch_one_okx_ticker("BTC-USDT", url=url, timeout_s=2.0)
            assert ticker.bid_px == 8888.88
            assert ticker.ask_px == 9999.99

    asyncio.run(run_test())
