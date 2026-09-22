#!/usr/bin/env python3
"""Concurrent POST /match load smoke test (no eligibility invention).

Uses a fixed sample US/India profile. Prints RPS, latency percentiles,
and status-code histogram.

Examples:
  python scripts/loadtest_match.py --url http://127.0.0.1:8000 --concurrency 20 --requests 200
  python scripts/loadtest_match.py --url https://example.vercel.app/api --path /match
"""

from __future__ import annotations

import argparse
import asyncio
import statistics
import sys
import time
from collections import Counter
from typing import Any

try:
    import httpx
except ImportError:
    print("httpx required: pip install httpx", file=sys.stderr)
    sys.exit(1)

# Fixed sample profiles — do not invent scheme rules; only exercise the API.
SAMPLE_PROFILES: dict[str, dict[str, Any]] = {
    "india": {
        "age": 68,
        "gender": "female",
        "country": "India",
        "state": "Kerala",
        "district": "Thiruvananthapuram",
        "monthly_household_income": 4000,
        "occupations": ["homemaker"],
        "categories": ["general"],
    },
    "us": {
        "age": 45,
        "gender": "male",
        "country": "United States",
        "state": "California",
        "annual_income": 35000,
        "occupations": ["worker"],
        "categories": ["general"],
    },
}


def _percentile(sorted_vals: list[float], p: float) -> float:
    if not sorted_vals:
        return 0.0
    k = (len(sorted_vals) - 1) * (p / 100.0)
    f = int(k)
    c = min(f + 1, len(sorted_vals) - 1)
    if f == c:
        return sorted_vals[f]
    return sorted_vals[f] + (sorted_vals[c] - sorted_vals[f]) * (k - f)


async def _one(
    client: httpx.AsyncClient,
    url: str,
    body: dict[str, Any],
    sem: asyncio.Semaphore,
) -> tuple[int, float]:
    async with sem:
        t0 = time.perf_counter()
        try:
            r = await client.post(url, json=body)
            status = r.status_code
        except Exception:  # noqa: BLE001
            status = 0
        elapsed_ms = (time.perf_counter() - t0) * 1000.0
        return status, elapsed_ms


async def run(args: argparse.Namespace) -> int:
    base = args.url.rstrip("/")
    path = args.path if args.path.startswith("/") else f"/{args.path}"
    url = f"{base}{path}"
    body = dict(SAMPLE_PROFILES[args.profile])
    if args.lang:
        body["lang"] = args.lang

    sem = asyncio.Semaphore(args.concurrency)
    limits = httpx.Limits(max_connections=args.concurrency + 10, max_keepalive_connections=args.concurrency)
    timeout = httpx.Timeout(args.timeout)

    latencies: list[float] = []
    statuses: Counter[int] = Counter()

    async with httpx.AsyncClient(limits=limits, timeout=timeout) as client:
        t_wall0 = time.perf_counter()
        tasks = [_one(client, url, body, sem) for _ in range(args.requests)]
        results = await asyncio.gather(*tasks)
        wall = time.perf_counter() - t_wall0

    for status, ms in results:
        statuses[status] += 1
        latencies.append(ms)

    latencies.sort()
    rps = args.requests / wall if wall > 0 else 0.0
    print(f"URL:          {url}")
    print(f"Profile:      {args.profile}")
    print(f"Requests:     {args.requests}")
    print(f"Concurrency:  {args.concurrency}")
    print(f"Wall time:    {wall:.3f}s")
    print(f"RPS:          {rps:.1f}")
    print(
        "Latency ms:   "
        f"p50={_percentile(latencies, 50):.1f}  "
        f"p95={_percentile(latencies, 95):.1f}  "
        f"p99={_percentile(latencies, 99):.1f}  "
        f"max={latencies[-1]:.1f}" if latencies else "Latency ms:   n/a"
    )
    if len(latencies) > 1:
        print(f"Latency mean: {statistics.mean(latencies):.1f} ms")
    print("Status codes:")
    for code, n in sorted(statuses.items()):
        label = "transport_error" if code == 0 else str(code)
        print(f"  {label}: {n}")
    return 0 if statuses.get(0, 0) == 0 and all(c < 500 for c in statuses) else 1


def main() -> None:
    p = argparse.ArgumentParser(description="Load-test Scheme Finder POST /match")
    p.add_argument("--url", default="http://127.0.0.1:8000", help="API base URL")
    p.add_argument("--path", default="/match", help="Match path (/match or /api/match)")
    p.add_argument("--concurrency", type=int, default=20)
    p.add_argument("--requests", type=int, default=100)
    p.add_argument("--timeout", type=float, default=30.0)
    p.add_argument("--profile", choices=sorted(SAMPLE_PROFILES), default="india")
    p.add_argument("--lang", default="en")
    args = p.parse_args()
    raise SystemExit(asyncio.run(run(args)))


if __name__ == "__main__":
    main()
