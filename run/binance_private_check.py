import os
import sys

from dotenv import load_dotenv
load_dotenv()

from adapters.binance_usdm_private import BinanceKeys, BinanceUsdmPrivateClient


def _need(name: str) -> str:
    v = os.getenv(name, "").strip()
    if not v:
        print(f"Missing env var: {name}")
        return ""
    return v


def main() -> int:
    base_url = os.getenv("BINANCE_USDM_BASE_URL", "https://demo-fapi.binance.com").strip()

    api_key = _need("BINANCE_USDM_API_KEY")
    api_secret = _need("BINANCE_USDM_API_SECRET")
    if not api_key or not api_secret:
        print("\nCreate a local .env (NOT committed) based on .env.example and put demo-trading keys there.")
        return 2

    c = BinanceUsdmPrivateClient(keys=BinanceKeys(api_key=api_key, api_secret=api_secret), base_url=base_url)

    print("Account V2...")
    acc = c.account_v2()
    # Print only a few fields to keep output readable:
    for k in ["totalWalletBalance", "availableBalance", "totalUnrealizedProfit", "totalMarginBalance"]:
        if k in acc:
            print(f"{k}: {acc[k]}")

    print("\nPositionRisk V2 (BTCUSDT)...")
    pr = c.position_risk_v2("BTCUSDT")
    # API returns a list
    if isinstance(pr, list) and pr:
        p0 = pr[0]
        for k in ["symbol", "positionAmt", "entryPrice", "unRealizedProfit", "leverage", "marginType"]:
            if k in p0:
                print(f"{k}: {p0[k]}")
    else:
        print("No positions returned (OK on a fresh demo account).")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())