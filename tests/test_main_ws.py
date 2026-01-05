import asyncio
import json

import pytest

from triarb.main import run_okx_ws_sample


def test_run_okx_ws_sample_from_local_server():
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
            text = await run_okx_ws_sample("BTC-USDT", url=url)
            assert "BTC-USDT" in text
            assert "8888.88" in text
            assert "9999.99" in text

    asyncio.run(run_test())
