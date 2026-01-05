from __future__ import annotations

EXCLUDED_ASSETS: list[str] = ["BTC", "ETH", "SOL", "XRP", "BNB", "TRX"]
DEFAULT_ASSETS: list[str] = ["DOGE", "ADA", "LINK", "LTC", "AVAX", "UNI", "BCH"]


def filter_assets(candidates: list[str], excluded: list[str]) -> list[str]:
    excluded_set = {asset.upper() for asset in excluded}
    result: list[str] = []
    for asset in candidates:
        upper = asset.upper()
        if upper in excluded_set:
            continue
        if upper not in result:
            result.append(upper)
    return result
