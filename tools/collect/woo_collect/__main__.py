import argparse
import json

from woo_collect.extract import extract
from woo_collect.fetch import client, fetch
from woo_collect.sources import DATA, load_sources


def main() -> None:
    parser = argparse.ArgumentParser(prog="python -m woo_collect", description="Fetch and clean Woo background sources.")
    parser.add_argument("step", choices=["fetch", "extract", "all"])
    parser.add_argument("--only", nargs="+", metavar="ID", help="limit to these source ids")
    parser.add_argument("--refresh", action="store_true", help="download again even if a raw file exists")
    args = parser.parse_args()

    sources = [s for s in load_sources() if not args.only or s.id in args.only]
    status: dict[str, dict[str, str]] = {s.id: {} for s in sources}

    if args.step in ("fetch", "all"):
        with client() as http:
            for s in sources:
                try:
                    status[s.id]["fetch"] = fetch(s, http, args.refresh)
                except Exception as e:  # one bad source must not stop the run
                    status[s.id]["fetch"] = f"error: {e}"
                print(f"fetch   {s.id:40} {status[s.id]['fetch']}")

    if args.step in ("extract", "all"):
        for s in sources:
            try:
                status[s.id]["extract"] = extract(s)
            except Exception as e:
                status[s.id]["extract"] = f"error: {e}"
            print(f"extract {s.id:40} {status[s.id]['extract']}")

    DATA.mkdir(exist_ok=True)
    (DATA / "last_run.json").write_text(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
