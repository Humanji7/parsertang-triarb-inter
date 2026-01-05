import asyncio
import json

import pytest

from triarb.main import run_okx_gate_spread_sample


def test_run_okx_gate_spread_sample_from_local_servers():
    async def run_test() -> None:
        websockets = pytest.importorskip("websockets")

        okx_message = {
            "arg": {"channel": "tickers", "instId": "BTC-USDT"},
            "data": [
                {
                    "instType": "SPOT",
                    "instId": "BTC-USDT",
                    "last": "9999.99",
                    "lastSz": "0.1",
                    "askPx": "100.0",
                    "askSz": "11",
                    "bidPx": "99.0",
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

        gate_message = {
            "time": 1606293275,
            "time_ms": 1606293275723,
            "channel": "spot.book_ticker",
            "event": "update",
            "result": {
                "t": 1606293275123,
                "u": 48733182,
                "s": "BTC_USDT",
                "b": "101.0",
                "B": "0.0003341504",
                "a": "102.0",
                "A": "0.09",
            },
        }

        async def okx_handler(websocket):
            await websocket.recv()
            await websocket.send(
                json.dumps({"event": "subscribe", "arg": {"channel": "tickers", "instId": "BTC-USDT"}})
            )
            await websocket.send(json.dumps(okx_message))

        async def gate_handler(websocket):
            await websocket.recv()
            await websocket.send(json.dumps({"event": "subscribe", "channel": "spot.book_ticker"}))
            await websocket.send(json.dumps(gate_message))

        async with websockets.serve(okx_handler, "localhost", 0) as okx_server:
            okx_port = okx_server.sockets[0].getsockname()[1]
            okx_url = f"ws://localhost:{okx_port}"
            async with websockets.serve(gate_handler, "localhost", 0) as gate_server:
                gate_port = gate_server.sockets[0].getsockname()[1]
                gate_url = f"ws://localhost:{gate_port}"
                text = await run_okx_gate_spread_sample(
                    okx_inst_id="BTC-USDT",
                    gate_inst_id="BTC_USDT",
                    okx_url=okx_url,
                    gate_url=gate_url,
                )
                assert "spread_pct=1.0" in text

    asyncio.run(run_test())
