from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


@dataclass(frozen=True)
class SymbolMeta:
    symbol: str
    tick_size: float
    step_size: float
    min_qty: float


class BinanceUsdmPublicClient:
    """
    Minimal public client for Binance USD-M Futures (no auth).
    Base URL: https://fapi.binance.com
    """

    def __init__(self, base_url: str = "https://fapi.binance.com", timeout_sec: int = 10) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout_sec = timeout_sec

    def _get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        url = f"{self.base_url}{path}"
        resp = requests.get(url, params=params, timeout=self.timeout_sec)
        resp.raise_for_status()
        return resp.json()

    def ping(self) -> None:
        # /fapi/v1/ping returns {}
        self._get("/fapi/v1/ping")

    def server_time_ms(self) -> int:
        data = self._get("/fapi/v1/time")
        return int(data["serverTime"])

    def exchange_info_symbol(self, symbol: str) -> SymbolMeta:
        data = self._get("/fapi/v1/exchangeInfo", params={"symbol": symbol})
        symbols = data.get("symbols", [])
        if not symbols:
            raise ValueError(f"Symbol not found in exchangeInfo: {symbol}")

        s0 = symbols[0]
        filters = {f["filterType"]: f for f in s0.get("filters", [])}

        price_filter = filters.get("PRICE_FILTER")
        lot_size = filters.get("LOT_SIZE")

        if not price_filter or not lot_size:
            raise ValueError(f"Missing PRICE_FILTER or LOT_SIZE for symbol: {symbol}")

        tick_size = float(price_filter["tickSize"])
        step_size = float(lot_size["stepSize"])
        min_qty = float(lot_size["minQty"])

        return SymbolMeta(symbol=symbol, tick_size=tick_size, step_size=step_size, min_qty=min_qty)