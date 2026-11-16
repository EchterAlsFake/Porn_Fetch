from .common import *


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--provider", action="append")
    parser.add_argument("--search", action="store_true")
    parser.add_argument("--extra", action="store_true")
    args = parser.parse_args()
    if args.extra:
        from .extra_cases import extras

        cases[:] = extras
    selected = [c for c in cases if not args.provider or c[0] in args.provider]
    if args.search:
        selected = [
            (s, None, None, None)
            for s in [c[0] for c in cases] + ["xfreehd"]
            if not args.provider or s in args.provider
        ]
    sem = asyncio.Semaphore(2)
    results = []

    async def one(case):
        async with sem:
            try:
                row = await asyncio.wait_for(runsearch(case[0]) if args.search else run(*case), 180)
            except Exception as e:
                row = {
                    "provider": case[0],
                    "kind": "search" if args.search else case[1],
                    "status": "FAIL",
                    "error": type(e).__name__ + ": " + str(e),
                }
            print(json.dumps(row), flush=True)
            results.append(row)

    await asyncio.gather(*(one(c) for c in selected))
    (OUTPUT / (("search" if args.search else "extras" if args.extra else "profiles") + ".json")).write_text(
        json.dumps(results, indent=2)
    )
    if any(row["status"] != "PASS" for row in results):
        raise SystemExit(1)


if __name__ == "__main__":
    asyncio.run(main())
