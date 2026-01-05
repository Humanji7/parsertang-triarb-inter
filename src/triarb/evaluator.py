from __future__ import annotations

from typing import Iterable


def compute_noptimal(
    depth: Iterable[tuple[float, float]],
    *,
    max_slip_pct: float,
) -> float:
    depth_list = list(depth)
    if not depth_list:
        return 0.0
    best_price = depth_list[0][0]
    total = 0.0
    for price, vol in depth_list:
        if ((price - best_price) / best_price) * 100 <= max_slip_pct:
            total += float(vol)
    return total
