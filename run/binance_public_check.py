from adapters.binance_usdm_public import BinanceUsdmPublicClient


def main() -> None:
    c = BinanceUsdmPublicClient()

    print("Ping...")
    c.ping()
    print("OK")

    t = c.server_time_ms()
    print(f"Server time (ms): {t}")

    meta = c.exchange_info_symbol("BTCUSDT")
    print("SymbolMeta:", meta)


if __name__ == "__main__":
    main()