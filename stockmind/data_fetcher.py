"""
Data Fetcher Module - Handles stock data retrieval from multiple sources

Supports A-shares (China), Hong Kong stocks, and US stocks with caching mechanism
"""

import json
import time
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union
from pathlib import Path
import requests


class DataFetcher:
    """Stock data fetcher with caching and multi-market support"""

    # API Endpoints
    AKSHARE_API = "https://query.sse.com.cn"
    YAHOO_API = "https://query1.finance.yahoo.com/v8/finance/chart"
    
    def __init__(self, cache_dir: str = ".stockmind_cache", cache_ttl: int = 300):
        """
        Initialize data fetcher
        
        Args:
            cache_dir: Cache directory path
            cache_ttl: Cache time-to-live in seconds (default: 5 minutes)
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.cache_ttl = cache_ttl
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })

    def _get_cache_key(self, symbol: str, market: str, period: str) -> str:
        """Generate cache key for request"""
        key = f"{market}_{symbol}_{period}_{datetime.now().strftime('%Y%m%d')}"
        return hashlib.md5(key.encode()).hexdigest()

    def _get_cache_path(self, cache_key: str) -> Path:
        """Get cache file path"""
        return self.cache_dir / f"{cache_key}.json"

    def _read_cache(self, cache_key: str) -> Optional[Dict]:
        """Read data from cache if valid"""
        cache_path = self._get_cache_path(cache_key)
        if not cache_path.exists():
            return None
        
        try:
            with open(cache_path, 'r', encoding='utf-8') as f:
                cached = json.load(f)
            
            # Check if cache is still valid
            cached_time = cached.get('_cached_at', 0)
            if time.time() - cached_time > self.cache_ttl:
                return None
            
            return cached.get('data')
        except (json.JSONDecodeError, KeyError):
            return None

    def _write_cache(self, cache_key: str, data: Dict):
        """Write data to cache"""
        cache_path = self._get_cache_path(cache_key)
        try:
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump({
                    '_cached_at': time.time(),
                    'data': data
                }, f, ensure_ascii=False, indent=2)
        except Exception:
            pass  # Cache write failure should not affect main functionality

    def _fetch_yahoo_data(self, symbol: str, period: str = "1mo") -> Dict:
        """
        Fetch stock data from Yahoo Finance
        
        Args:
            symbol: Stock symbol (e.g., AAPL, TSLA, 0700.HK)
            period: Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
            
        Returns:
            Dictionary containing stock data
        """
        interval_map = {
            "1d": "1m", "5d": "5m", "1mo": "1d", "3mo": "1d",
            "6mo": "1d", "1y": "1d", "2y": "1wk", "5y": "1wk"
        }
        interval = interval_map.get(period, "1d")
        
        url = f"{self.YAHOO_API}/{symbol}"
        params = {
            "period1": int((datetime.now() - self._parse_period(period)).timestamp()),
            "period2": int(datetime.now().timestamp()),
            "interval": interval,
            "events": "history"
        }
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            if "chart" not in data or "result" not in data["chart"] or not data["chart"]["result"]:
                raise ValueError(f"No data available for symbol: {symbol}")
            
            result = data["chart"]["result"][0]
            timestamps = result.get("timestamp", [])
            quote = result.get("indicators", {}).get("quote", [{}])[0]
            
            # Process data
            processed_data = []
            for i, ts in enumerate(timestamps):
                if all(k in quote and quote[k][i] is not None for k in ["open", "high", "low", "close", "volume"]):
                    processed_data.append({
                        "date": datetime.fromtimestamp(ts).strftime("%Y-%m-%d"),
                        "open": round(quote["open"][i], 4),
                        "high": round(quote["high"][i], 4),
                        "low": round(quote["low"][i], 4),
                        "close": round(quote["close"][i], 4),
                        "volume": int(quote["volume"][i])
                    })
            
            meta = result.get("meta", {})
            return {
                "symbol": symbol,
                "currency": meta.get("currency", "USD"),
                "exchange": meta.get("exchangeName", "Unknown"),
                "data": processed_data,
                "current_price": meta.get("regularMarketPrice"),
                "previous_close": meta.get("previousClose"),
                "market_state": meta.get("marketState", "UNKNOWN")
            }
            
        except requests.RequestException as e:
            raise ConnectionError(f"Failed to fetch data from Yahoo Finance: {str(e)}")
        except (KeyError, IndexError) as e:
            raise ValueError(f"Invalid data format received: {str(e)}")

    def _parse_period(self, period: str) -> datetime:
        """Parse period string to datetime"""
        now = datetime.now()
        period_map = {
            "1d": now - timedelta(days=1),
            "5d": now - timedelta(days=5),
            "1mo": now - timedelta(days=30),
            "3mo": now - timedelta(days=90),
            "6mo": now - timedelta(days=180),
            "1y": now - timedelta(days=365),
            "2y": now - timedelta(days=730),
            "5y": now - timedelta(days=1825)
        }
        return period_map.get(period, now - timedelta(days=30))

    def get_stock_data(self, symbol: str, market: str = "us", period: str = "1mo", 
                       use_cache: bool = True) -> Dict:
        """
        Get stock data with caching
        
        Args:
            symbol: Stock symbol
            market: Market type (us, hk, cn)
            period: Time period
            use_cache: Whether to use cache
            
        Returns:
            Stock data dictionary
        """
        # Normalize symbol based on market
        normalized_symbol = self._normalize_symbol(symbol, market)
        
        # Check cache
        cache_key = self._get_cache_key(normalized_symbol, market, period)
        if use_cache:
            cached_data = self._read_cache(cache_key)
            if cached_data:
                return cached_data
        
        # Fetch fresh data
        data = self._fetch_yahoo_data(normalized_symbol, period)
        data["market"] = market
        
        # Write to cache
        if use_cache:
            self._write_cache(cache_key, data)
        
        return data

    def _normalize_symbol(self, symbol: str, market: str) -> str:
        """Normalize symbol for different markets"""
        symbol = symbol.upper().strip()
        
        if market == "hk":
            # Hong Kong stocks: add .HK suffix
            if not symbol.endswith(".HK"):
                symbol = f"{symbol}.HK"
        elif market == "cn":
            # A-shares: add .SS for Shanghai, .SZ for Shenzhen
            if symbol.startswith("6"):
                if not symbol.endswith(".SS"):
                    symbol = f"{symbol}.SS"
            elif symbol.startswith(("0", "3")):
                if not symbol.endswith(".SZ"):
                    symbol = f"{symbol}.SZ"
        # US stocks typically don't need suffix
        
        return symbol

    def search_stocks(self, query: str) -> List[Dict]:
        """
        Search for stocks by name or symbol
        
        Args:
            query: Search query
            
        Returns:
            List of matching stocks
        """
        # Yahoo Finance search API
        url = "https://query1.finance.yahoo.com/v1/finance/search"
        params = {
            "q": query,
            "quotesCount": 10,
            "newsCount": 0,
            "listsCount": 0
        }
        
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            quotes = data.get("quotes", [])
            results = []
            for quote in quotes:
                results.append({
                    "symbol": quote.get("symbol"),
                    "name": quote.get("shortname") or quote.get("longname"),
                    "exchange": quote.get("exchange"),
                    "type": quote.get("quoteType"),
                    "sector": quote.get("sector"),
                    "industry": quote.get("industry")
                })
            
            return results
            
        except requests.RequestException:
            return []

    def get_market_summary(self) -> Dict:
        """Get major market indices summary"""
        indices = {
            "^GSPC": "S&P 500",
            "^DJI": "Dow Jones",
            "^IXIC": "NASDAQ",
            "^HSI": "Hang Seng",
            "000001.SS": "SSE Composite",
            "399001.SZ": "SZSE Component"
        }
        
        summary = {}
        for symbol, name in indices.items():
            try:
                data = self._fetch_yahoo_data(symbol, "1d")
                summary[name] = {
                    "symbol": symbol,
                    "price": data.get("current_price"),
                    "change": round(data.get("current_price", 0) - data.get("previous_close", 0), 2),
                    "change_percent": round(
                        ((data.get("current_price", 0) - data.get("previous_close", 0)) / 
                         data.get("previous_close", 1)) * 100, 2
                    ) if data.get("previous_close") else 0
                }
            except Exception:
                continue
        
        return summary
