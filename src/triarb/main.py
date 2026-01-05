from __future__ import annotations

import asyncio

from triarb.alerts import format_signal
from triarb.evaluator import compute_net_profit_pct, compute_noptimal
from triarb.feeder import mock_orderbook_depth
from triarb.gate_ws import GATE_PUBLIC_WS_URL, fetch_one_gate_book_ticker
from triarb.okx_ws import OKX_PUBLIC_WS_URL, fetch_one_okx_ticker
from triarb.spread import compute_spread_pct


def run_mock_pipeline() -> str | None:
    depth = mock_orderbook_depth()
    n_opt = compute_noptimal(depth, max_slip_pct=0.05)
    if n_opt <= 0:
        return None
    gross = 0.6
    fees = 0.2
    slip = 0.05
    net = compute_net_profit_pct(gross, fees, slip)
    if net <= 0.3:
        return None
    return format_signal("bybit", "okx", "USDT", "ADA", "DOT", "ARBITRUM", n_opt, net)


async def run_okx_ws_sample(inst_id: str, url: str = OKX_PUBLIC_WS_URL) -> str:
    ticker = await fetch_one_okx_ticker(inst_id, url=url)
    return f"{ticker.inst_id} bid={ticker.bid_px} ask={ticker.ask_px}"


async def run_gate_ws_sample(inst_id: str, url: str = GATE_PUBLIC_WS_URL) -> str:
    ticker = await fetch_one_gate_book_ticker(inst_id, url=url)
    return f"{ticker.inst_id} bid={ticker.bid_px} ask={ticker.ask_px}"


async def run_okx_gate_spread_sample(
    okx_inst_id: str,
    gate_inst_id: str,
    okx_url: str = OKX_PUBLIC_WS_URL,
    gate_url: str = GATE_PUBLIC_WS_URL,
) -> str:
    okx_task = asyncio.create_task(fetch_one_okx_ticker(okx_inst_id, url=okx_url))
    gate_task = asyncio.create_task(fetch_one_gate_book_ticker(gate_inst_id, url=gate_url))
    okx_ticker, gate_ticker = await asyncio.gather(okx_task, gate_task)
    spread_pct = compute_spread_pct(buy_ask=okx_ticker.ask_px, sell_bid=gate_ticker.bid_px)
    return f"{okx_ticker.inst_id}->{gate_ticker.inst_id} spread_pct={round(spread_pct, 4)}"
