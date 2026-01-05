from __future__ import annotations


class FeeCache:
    def __init__(self) -> None:
        self.trade_fees: dict[str, float] = {}

    def set_trade_fee(self, exchange: str, fee: float) -> None:
        self.trade_fees[exchange] = fee

    def get_trade_fee(self, exchange: str) -> float | None:
        return self.trade_fees.get(exchange)
