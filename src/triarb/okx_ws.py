from __future__ import annotations

import asyncio
import json
import time
from dataclasses import dataclass

OKX_PUBLIC_WS_URL = "wss://ws.okx.com:8443/ws/v5/public"


@dataclass(frozen=True)
class Ticker:
    inst_id: str
    bid_px: float
    ask_px: float
    ts_ms: int


def build_okx_subscribe_message(inst_id: str, channel: str = "tickers") -> dict:
    return {"op": "subscribe", "args": [{"channel": channel, "instId": inst_id}]}


def parse_okx_ticker_message(message: dict) -> Ticker | None:
    arg = message.get("arg")
    if not arg or arg.get("channel") != "tickers":
        return None
    data = message.get("data")
    if not data:
        return None
    item = data[0]
    try:
        return Ticker(
            inst_id=item["instId"],
            bid_px=float(item["bidPx"]),
            ask_px=float(item["askPx"]),
            ts_ms=int(item["ts"]),
        )
    except (KeyError, TypeError, ValueError):
        return None


async def fetch_one_okx_ticker(inst_id: str, url: str = OKX_PUBLIC_WS_URL, timeout_s: float = 5.0) -> Ticker:
    try:
        import websockets
    except Exception as exc:  # pragma: no cover - depends on optional dependency
        raise RuntimeError("websockets dependency is required for live WS") from exc

    subscribe = build_okx_subscribe_message(inst_id)
    deadline = time.monotonic() + timeout_s
    async with websockets.connect(url, ping_interval=20, ping_timeout=20) as ws:
        await ws.send(json.dumps(subscribe))
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise TimeoutError("OKX ticker timeout")
            raw = await asyncio.wait_for(ws.recv(), timeout=remaining)
            try:
                message = json.loads(raw)
            except json.JSONDecodeError:
                continue
            ticker = parse_okx_ticker_message(message)
            if ticker is not None:
                return ticker
