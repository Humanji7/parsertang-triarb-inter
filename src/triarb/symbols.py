from __future__ import annotations


def build_inst_id(exchange: str, asset: str, base: str) -> str:
    exchange_lower = exchange.lower()
    asset_upper = asset.upper()
    base_upper = base.upper()
    if exchange_lower == "okx":
        return f"{asset_upper}-{base_upper}"
    if exchange_lower == "gate":
        return f"{asset_upper}_{base_upper}"
    raise ValueError(f"unsupported exchange: {exchange}")
