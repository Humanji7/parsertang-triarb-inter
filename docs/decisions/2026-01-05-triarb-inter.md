# Triarb-Inter Decisions (2026-01-05)

## Scope
- Focus on **intra-exchange triangle** first (Gate), then expand outward.
- Inter-exchange spread remains separate from triangle logic.

## Why Gate First
- Single exchange reduces WS failure points.
- Faster to validate triangle hypothesis before scaling complexity.

## Triangle Structure
- Triangle requires A/USDT + A/B + B/USDT.
- Gate rarely has A/B for arbitrary alts.
- Use **bridge asset** (BTC, optionally ETH):
  - USDT -> A -> BTC -> USDT

## Asset Policy
- Exclude top-6 (BTC, ETH, SOL, XRP, BNB, TRX) from inter-exchange scanning.
- Allow BTC/ETH **only as bridge** inside triangle.

## WS Strategy
- Avoid per-pair WS connections (timeouts/limits).
- Prefer **single WS connection with multi-subscribe**.
- For triangle, subscribe to three pairs in one session.

## Filters
- Require net-profit >= 0.3%.
- Include per-trade fee and slippage in net calculation.

## Operational Notes
- Timeouts and error callbacks added; skip failed legs.
- Concurrency limited at fetch-level (when used).

