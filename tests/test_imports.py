def test_imports():
    from adapters.binance_usdm_public import BinanceUsdmPublicClient
    from adapters.binance_usdm_private import BinanceUsdmPrivateClient, BinanceKeys

    assert BinanceUsdmPublicClient
    assert BinanceUsdmPrivateClient
    assert BinanceKeys