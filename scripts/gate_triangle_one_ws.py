import argparse
import asyncio

from triarb.main import run_gate_triangle_filtered_ws


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--asset", default="ADA")
    parser.add_argument("--base", default="USDT")
    parser.add_argument("--bridge", default="BTC")
    parser.add_argument("--fee", type=float, default=0.1)
    parser.add_argument("--slip", type=float, default=0.05)
    parser.add_argument("--min-net", type=float, default=0.3)
    parser.add_argument("--timeout", type=float, default=10.0)
    args = parser.parse_args()

    async def run() -> None:
        rows = await run_gate_triangle_filtered_ws(
            a_asset=args.asset,
            bridge_asset=args.bridge,
            base=args.base,
            fee_pct_per_trade=args.fee,
            slippage_pct_per_trade=args.slip,
            min_net_pct=args.min_net,
            timeout_s=args.timeout,
        )
        print(rows)

    asyncio.run(run())


if __name__ == "__main__":
    main()
