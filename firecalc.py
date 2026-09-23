#!/usr/bin/env python3
"""firecalc - a tiny FIRE number calculator. Python stdlib only, one file.

Computes your FI number from annual spending and a safe withdrawal rate,
then works out how many years until you get there given current savings,
annual contributions and a real (inflation-adjusted) return. Also prints a
coast-FI number: what you need today to hit FI at target age with zero
further contributions.

Examples:
  python3 firecalc.py --spending 40000 --savings 150000 --contrib 20000
  python3 firecalc.py --spending 40000 --savings 150000 --contrib 20000 --age 32 --target-age 65
  python3 firecalc.py --spending 40000 --json
"""
import argparse
import json
import math
import sys


def years_to_fi(savings, contrib, target, rate):
    """Solve S*(1+r)^n + c*(((1+r)^n - 1)/r) = F for n. Returns None if unreachable."""
    if savings >= target:
        return 0.0
    denom = savings + contrib / rate if rate > 0 else savings
    if denom <= 0:
        return None
    if rate <= 0:
        return None if contrib <= 0 else (target - savings) / contrib
    a = (target + contrib / rate) / denom
    if a <= 0:
        return None
    n = math.log(a) / math.log(1 + rate)
    return n if n > 0 else 0.0


def main(argv=None):
    p = argparse.ArgumentParser(description="Tiny FIRE number calculator (stdlib only).")
    p.add_argument("--spending", type=float, required=True, help="annual spending (currency units)")
    p.add_argument("--savings", type=float, default=0.0, help="current investable savings")
    p.add_argument("--contrib", type=float, default=0.0, help="annual contributions")
    p.add_argument("--return", dest="rate", type=float, default=0.05, help="real annual return, default 0.05")
    p.add_argument("--swr", type=float, default=4.0, help="safe withdrawal rate percent, default 4")
    p.add_argument("--age", type=float, help="current age (enables coast-FI)")
    p.add_argument("--target-age", type=float, help="target age (enables coast-FI)")
    p.add_argument("--json", action="store_true", help="machine-readable output")
    args = p.parse_args(argv)

    if args.spending <= 0:
        p.error("--spending must be positive")
    if not (0 < args.swr <= 25):
        p.error("--swr must be between 0 and 25 percent")
    if args.rate < -0.5 or args.rate > 0.3:
        p.error("--return must be a sane real rate, e.g. 0.05")

    fi_number = args.spending / (args.swr / 100.0)
    n = years_to_fi(args.savings, args.contrib, fi_number, args.rate)

    coast = None
    if args.age is not None and args.target_age is not None:
        yrs = args.target_age - args.age
        if yrs > 0:
            coast = fi_number / ((1 + args.rate) ** yrs)

    out = {
        "fi_number": round(fi_number, 2),
        "years_to_fi": round(n, 1) if n is not None else None,
        "coast_fi_today": round(coast, 2) if coast is not None else None,
        "assumptions": {
            "annual_spending": args.spending,
            "savings": args.savings,
            "annual_contrib": args.contrib,
            "real_return": args.rate,
            "swr_percent": args.swr,
        },
    }

    if args.json:
        print(json.dumps(out, indent=2))
        return 0

    print(f"FIRE number:      {out['fi_number']:>14,.0f}")
    if out["years_to_fi"] is None:
        print("Years to FI:      never at these inputs (raise contributions or return)")
    else:
        print(f"Years to FI:      {out['years_to_fi']:>14,.1f}")
    if out["coast_fi_today"] is not None:
        print(f"Coast FI today:   {out['coast_fi_today']:>14,.0f}")
    print(f"(assumes {args.swr:g}% withdrawal rate, {args.rate * 100:g}% real return)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
