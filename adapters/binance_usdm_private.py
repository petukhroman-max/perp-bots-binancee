from __future__ import annotations

import hashlib
import hmac
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional
from urllib.parse import urlencode

import requests


@dataclass(frozen=True)
class BinanceKeys:
    api_key: str
    api_secret: str


class BinanceUsdmPrivateClient:
    """
    Minimal signed (USER_DATA) client for Binance USD-M Futures.
    Designed for READ-ONLY checks first: account / balance / positions.

    Testnet REST base URL (per docs): https://demo-fapi.binance.com
    """

    def __init__(
        self,
        keys: BinanceKeys,
        base_url: str = "https://demo-fapi.binance.com",
        timeout_sec: int = 10,
        recv_window_ms: int = 5000,
    ) -> None:
        self.keys = keys
        self.base_url = base_url.rstrip("/")
        self.timeout_sec = timeout_sec
        self.recv_window_ms = recv_window_ms

    def _ts_ms(self) -> int:
        return int(time.time() * 1000)

    def _sign(self, params: Dict[str, Any]) -> str:
        # Binance requires signature HMAC SHA256 over the query string.
        # Signature should be appended at the end.
        query = urlencode(params, doseq=True)
        sig = hmac.new(
            self.keys.api_secret.encode("utf-8"),
            query.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        return f"{query}&signature={sig}"

    def _signed_get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        p: Dict[str, Any] = dict(params or {})
        p["timestamp"] = self._ts_ms()
        p.setdefault("recvWindow", self.recv_window_ms)

        signed_qs = self._sign(p)
        url = f"{self.base_url}{path}?{signed_qs}"

        headers = {"X-MBX-APIKEY": self.keys.api_key}
        resp = requests.get(url, headers=headers, timeout=self.timeout_sec)
        resp.raise_for_status()
        return resp.json()

    # ---- READ-ONLY endpoints ----

    def account_v2(self) -> Any:
        # GET /fapi/v2/account
        return self._signed_get("/fapi/v2/account")

    def balance_v2(self) -> Any:
        # GET /fapi/v2/balance
        return self._signed_get("/fapi/v2/balance")

    def position_risk_v2(self, symbol: Optional[str] = None) -> Any:
        # GET /fapi/v2/positionRisk
        params: Dict[str, Any] = {}
        if symbol:
            params["symbol"] = symbol
        return self._signed_get("/fapi/v2/positionRisk", params=params)