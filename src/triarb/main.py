from __future__ import annotations

from triarb.alerts import format_signal
from triarb.evaluator import compute_net_profit_pct, compute_noptimal
from triarb.feeder import mock_orderbook_depth
from triarb.okx_ws import OKX_PUBLIC_WS_URL, fetch_one_okx_ticker


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
