from __future__ import annotations

import asyncio

from triarb.alerts import format_signal
from triarb.evaluator import compute_net_profit_pct, compute_noptimal
from triarb.feeder import mock_orderbook_depth
from triarb.gate_ws import GATE_PUBLIC_WS_URL, fetch_one_gate_book_ticker
from triarb.okx_ws import OKX_PUBLIC_WS_URL, fetch_one_okx_ticker
from triarb.filters import should_signal
from triarb.spread import compute_spread_pct
from triarb.symbols import build_inst_id
from triarb.triangle import TriangleQuotes, compute_triangle_net_pct
from triarb.triangle_candidates import (
    build_gate_triangle_candidates,
    build_gate_triangle_candidates_with_bridge,
)


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


async def run_okx_gate_spread_batch(
    assets: list[str],
    base: str,
    okx_url: str = OKX_PUBLIC_WS_URL,
    gate_url: str = GATE_PUBLIC_WS_URL,
    fetch_okx=fetch_one_okx_ticker,
    fetch_gate=fetch_one_gate_book_ticker,
) -> list[str]:
    async def one(asset: str) -> str:
        okx_inst = build_inst_id("okx", asset, base)
        gate_inst = build_inst_id("gate", asset, base)
        okx_ticker = await fetch_okx(okx_inst, url=okx_url)
        gate_ticker = await fetch_gate(gate_inst, url=gate_url)
        spread_pct = compute_spread_pct(buy_ask=okx_ticker.ask_px, sell_bid=gate_ticker.bid_px)
        return f"{okx_ticker.inst_id}->{gate_ticker.inst_id} spread_pct={round(spread_pct, 4)}"

    tasks = [asyncio.create_task(one(asset)) for asset in assets]
    return await asyncio.gather(*tasks)


async def run_okx_gate_spread_filtered(
    assets: list[str],
    base: str,
    fee_pct: float,
    slippage_pct: float,
    min_net_pct: float,
    okx_url: str = OKX_PUBLIC_WS_URL,
    gate_url: str = GATE_PUBLIC_WS_URL,
    fetch_okx=fetch_one_okx_ticker,
    fetch_gate=fetch_one_gate_book_ticker,
) -> list[str]:
    async def one(asset: str) -> str | None:
        try:
            okx_inst = build_inst_id("okx", asset, base)
            gate_inst = build_inst_id("gate", asset, base)
            okx_ticker = await fetch_okx(okx_inst, url=okx_url)
            gate_ticker = await fetch_gate(gate_inst, url=gate_url)
            spread_pct = compute_spread_pct(buy_ask=okx_ticker.ask_px, sell_bid=gate_ticker.bid_px)
        except Exception:
            return None
        if not should_signal(spread_pct, fee_pct, slippage_pct, min_net_pct):
            return None
        net_pct = round(spread_pct - fee_pct - slippage_pct, 4)
        return f"{okx_ticker.inst_id}->{gate_ticker.inst_id} net_pct={net_pct}"

    tasks = [asyncio.create_task(one(asset)) for asset in assets]
    rows = await asyncio.gather(*tasks)
    return [row for row in rows if row is not None]


async def run_gate_triangle_filtered(
    a_asset: str,
    b_asset: str,
    base: str,
    fee_pct_per_trade: float,
    slippage_pct_per_trade: float,
    min_net_pct: float,
    timeout_s: float | None = None,
    gate_url: str = GATE_PUBLIC_WS_URL,
    fetch_gate=fetch_one_gate_book_ticker,
    on_error=None,
) -> list[str]:
    a_usdt = build_inst_id("gate", a_asset, base)
    a_b = build_inst_id("gate", a_asset, b_asset)
    b_usdt = build_inst_id("gate", b_asset, base)

    async def safe_fetch(inst_id: str):
        try:
            if timeout_s is None:
                return await fetch_gate(inst_id, url=gate_url)
            return await fetch_gate(inst_id, url=gate_url, timeout_s=timeout_s)
        except Exception as exc:
            if on_error is not None:
                on_error(inst_id, exc)
            return None

    tasks = [asyncio.create_task(safe_fetch(sym)) for sym in (a_usdt, a_b, b_usdt)]
    tickers = await asyncio.gather(*tasks)
    if any(ticker is None for ticker in tickers):
        return []
    a_usdt_ticker, a_b_ticker, b_usdt_ticker = tickers
    quotes = TriangleQuotes(
        a_usdt_ask=a_usdt_ticker.ask_px,
        a_b_bid=a_b_ticker.bid_px,
        b_usdt_bid=b_usdt_ticker.bid_px,
    )
    net_pct = compute_triangle_net_pct(quotes, fee_pct_per_trade, slippage_pct_per_trade)
    if net_pct < min_net_pct:
        return []
    return [f"{a_asset}->{b_asset}->{base} net_pct={round(net_pct, 2)}"]


async def run_gate_triangle_batch(
    assets: list[str],
    base: str,
    fee_pct_per_trade: float,
    slippage_pct_per_trade: float,
    min_net_pct: float,
    available_pairs: set[str] | None = None,
    max_triangles: int | None = None,
    timeout_s: float | None = None,
    gate_url: str = GATE_PUBLIC_WS_URL,
    fetch_gate=fetch_one_gate_book_ticker,
    on_error=None,
) -> list[str]:
    if available_pairs is not None:
        candidates = build_gate_triangle_candidates(assets, base=base, available_pairs=available_pairs)
    else:
        assets_upper = [asset.upper() for asset in assets]
        candidates = [(a, b) for a in assets_upper for b in assets_upper if a != b]
    if max_triangles is not None:
        candidates = candidates[: max_triangles]
    rows: list[str] = []
    for a_asset, b_asset in candidates:
        rows.extend(
            await run_gate_triangle_filtered(
                a_asset=a_asset,
                b_asset=b_asset,
                base=base,
                fee_pct_per_trade=fee_pct_per_trade,
                slippage_pct_per_trade=slippage_pct_per_trade,
                min_net_pct=min_net_pct,
                timeout_s=timeout_s,
                gate_url=gate_url,
                fetch_gate=fetch_gate,
                on_error=on_error,
            )
        )
    return rows


async def run_gate_triangle_batch_bridge(
    assets: list[str],
    base: str,
    bridge: str,
    fee_pct_per_trade: float,
    slippage_pct_per_trade: float,
    min_net_pct: float,
    available_pairs: set[str] | None = None,
    max_triangles: int | None = None,
    timeout_s: float | None = None,
    gate_url: str = GATE_PUBLIC_WS_URL,
    fetch_gate=fetch_one_gate_book_ticker,
    on_error=None,
) -> list[str]:
    if available_pairs is None:
        assets_upper = [asset.upper() for asset in assets]
        candidates = [(a, bridge.upper()) for a in assets_upper if a != bridge.upper()]
    else:
        candidates = build_gate_triangle_candidates_with_bridge(
            assets=assets,
            base=base,
            bridge=bridge,
            available_pairs=available_pairs,
        )
    if max_triangles is not None:
        candidates = candidates[: max_triangles]
    rows: list[str] = []
    for a_asset, bridge_asset in candidates:
        rows.extend(
            await run_gate_triangle_filtered(
                a_asset=a_asset,
                b_asset=bridge_asset,
                base=base,
                fee_pct_per_trade=fee_pct_per_trade,
                slippage_pct_per_trade=slippage_pct_per_trade,
                min_net_pct=min_net_pct,
                timeout_s=timeout_s,
                gate_url=gate_url,
                fetch_gate=fetch_gate,
                on_error=on_error,
            )
        )
    return rows
