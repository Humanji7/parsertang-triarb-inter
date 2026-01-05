from __future__ import annotations


def mock_orderbook_depth() -> list[tuple[float, float]]:
    return [
        (1.00, 1000.0),
        (1.01, 1000.0),
    ]
