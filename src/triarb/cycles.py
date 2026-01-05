from __future__ import annotations


def build_cycles(coins: list[str], base: str) -> list[tuple[str, str, str, str]]:
    cycles: list[tuple[str, str, str, str]] = []
    for i, x in enumerate(coins):
        for j, y in enumerate(coins):
            if i == j:
                continue
            cycles.append((base, x, y, base))
    return cycles
