from __future__ import annotations


def format_signal(ex_a, ex_b, base, x, y, network, n_opt, net_pct):
    return (
        "🚨 TRIARB INTER\n"
        f"Биржи: {ex_a.upper()} → {ex_b.upper()}\n"
        f"Цепочка: {base} → {x} → {y} → {base}\n"
        f"Сеть: {network}\n"
        f"NOptimal: {n_opt} {base}\n"
        f"ΠNet: +{net_pct:.2f}%"
    )
