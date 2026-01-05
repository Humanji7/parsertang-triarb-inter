from __future__ import annotations

import asyncio
import json
import time
from dataclasses import dataclass

GATE_PUBLIC_WS_URL = "wss://api.gateio.ws/ws/v4/"


@dataclass(frozen=True)
class BookTicker:
    inst_id: str
    bid_px: float
    ask_px: float
    ts_ms: int


def build_gate_subscribe_message(inst_id: str, channel: str = "spot.book_ticker") -> dict:
    return {
        "time": int(time.time()),
        "channel": channel,
        "event": "subscribe",
        "payload": [inst_id],
    }


def parse_gate_book_ticker_message(message: dict) -> BookTicker | None:
    if message.get("channel") != "spot.book_ticker":
        return None
    if message.get("event") != "update":
        return None
    result = message.get("result")
    if not result:
        return None
    try:
        return BookTicker(
            inst_id=result["s"],
            bid_px=float(result["b"]),
            ask_px=float(result["a"]),
            ts_ms=int(result["t"]),
        )
    except (KeyError, TypeError, ValueError):
        return None


async def fetch_one_gate_book_ticker(
    inst_id: str,
    url: str = GATE_PUBLIC_WS_URL,
    timeout_s: float = 5.0,
) -> BookTicker:
    try:
        import websockets
    except Exception as exc:  # pragma: no cover - depends on optional dependency
        raise RuntimeError("websockets dependency is required for live WS") from exc

    subscribe = build_gate_subscribe_message(inst_id)
    deadline = time.monotonic() + timeout_s
    async with websockets.connect(url, ping_interval=20, ping_timeout=20) as ws:
        await ws.send(json.dumps(subscribe))
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise TimeoutError("Gate book ticker timeout")
            raw = await asyncio.wait_for(ws.recv(), timeout=remaining)
            try:
                message = json.loads(raw)
            except json.JSONDecodeError:
                continue
            ticker = parse_gate_book_ticker_message(message)
            if ticker is not None:
                return ticker


async def fetch_gate_book_tickers(
    inst_ids: list[str],
    url: str = GATE_PUBLIC_WS_URL,
    timeout_s: float = 5.0,
    allow_partial: bool = False,
) -> dict[str, BookTicker]:
    try:
        import websockets
    except Exception as exc:  # pragma: no cover - depends on optional dependency
        raise RuntimeError("websockets dependency is required for live WS") from exc

    subscribe = build_gate_subscribe_message(inst_ids[0])
    subscribe["payload"] = list(inst_ids)
    deadline = time.monotonic() + timeout_s
    results: dict[str, BookTicker] = {}
    async with websockets.connect(url, ping_interval=20, ping_timeout=20) as ws:
        await ws.send(json.dumps(subscribe))
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                if allow_partial:
                    return results
                raise TimeoutError("Gate book tickers timeout")
            try:
                raw = await asyncio.wait_for(ws.recv(), timeout=remaining)
            except asyncio.TimeoutError:
                if allow_partial:
                    return results
                raise
            except Exception:
                if allow_partial:
                    return results
                raise
            try:
                message = json.loads(raw)
            except json.JSONDecodeError:
                continue
            ticker = parse_gate_book_ticker_message(message)
            if ticker is None:
                continue
            if ticker.inst_id in inst_ids:
                results[ticker.inst_id] = ticker
            if len(results) == len(inst_ids):
                return results
