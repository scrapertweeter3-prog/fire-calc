# firecalc

Tiny FIRE number calculator in one Python file. Standard library only: no install, no dependencies.

## What it does

- Computes your FIRE number from annual spending and a safe withdrawal rate (`--swr`, default 4%).
- Solves years-to-FI from current savings, annual contributions, and a real (inflation-adjusted) return.
- Optional coast-FI: what you need invested today to hit FI at a target age with no further contributions.
- `--json` for machine-readable output, sane input validation, and script-friendly exit codes.

## Usage

```
$ python3 firecalc.py --spending 40000 --savings 150000 --contrib 20000
FIRE number:           1,000,000
Years to FI:                19.1
(assumes 4% withdrawal rate, 5% real return)

$ python3 firecalc.py --spending 40000 --savings 150000 --contrib 20000 --age 32 --target-age 65
FIRE number:           1,000,000
Years to FI:                19.1
Coast FI today:          199,873
(assumes 4% withdrawal rate, 5% real return)

$ python3 firecalc.py --spending 40000 --json
```

## The math

FI number = annual spending / safe withdrawal rate. Years to FI solves
`S*(1+r)^n + c*(((1+r)^n - 1)/r) = F` in closed form. Coast FI = `F / (1+r)^(target - now)`.
All rates are real (inflation-adjusted), so results are in today's money.

A calculator is the easy part; the withdrawal rate you pick is where the risk lives.
For withdrawal strategies, sequence-of-returns math, and practical FIRE guides grounded
in real numbers, see [FIREnomics](https://firenomics.com/).

## License

MIT
