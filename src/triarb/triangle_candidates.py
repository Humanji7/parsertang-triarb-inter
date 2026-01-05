from __future__ import annotations


def build_gate_triangle_candidates(
    assets: list[str],
    base: str,
    available_pairs: set[str],
) -> list[tuple[str, str]]:
    base_upper = base.upper()
    assets_upper = [asset.upper() for asset in assets]
    candidates: list[tuple[str, str]] = []
    for a in assets_upper:
        a_usdt = f"{a}_{base_upper}"
        if a_usdt not in available_pairs:
            continue
        for b in assets_upper:
            if b == a:
                continue
            b_usdt = f"{b}_{base_upper}"
            a_b = f"{a}_{b}"
            if a_b in available_pairs and b_usdt in available_pairs:
                candidates.append((a, b))
    return candidates


def build_gate_triangle_candidates_with_bridge(
    assets: list[str],
    base: str,
    bridge: str,
    available_pairs: set[str],
) -> list[tuple[str, str]]:
    base_upper = base.upper()
    bridge_upper = bridge.upper()
    assets_upper = [asset.upper() for asset in assets]
    candidates: list[tuple[str, str]] = []
    bridge_base = f"{bridge_upper}_{base_upper}"
    if bridge_base not in available_pairs:
        return []
    for a in assets_upper:
        a_usdt = f"{a}_{base_upper}"
        a_bridge = f"{a}_{bridge_upper}"
        if a_usdt in available_pairs and a_bridge in available_pairs:
            candidates.append((a, bridge_upper))
    return candidates
