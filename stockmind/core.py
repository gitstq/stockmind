"""
Core Module - Main StockMind functionality

Provides high-level interface for stock analysis operations
"""

from typing import Dict, List, Optional
from .data_fetcher import DataFetcher
from .analyzer import TechnicalAnalyzer
from .ai_analyzer import AIAnalyzer


class StockMind:
    """Main StockMind class for stock analysis"""

    def __init__(self, cache_dir: str = ".stockmind_cache", 
                 ai_provider: Optional[str] = None,
                 ai_api_key: Optional[str] = None):
        """
        Initialize StockMind
        
        Args:
            cache_dir: Cache directory path
            ai_provider: AI provider for analysis (openai, anthropic, deepseek, glm)
            ai_api_key: API key for AI provider
        """
        self.data_fetcher = DataFetcher(cache_dir=cache_dir)
        self.ai_analyzer = None
        
        if ai_provider:
            try:
                self.ai_analyzer = AIAnalyzer(provider=ai_provider, api_key=ai_api_key)
            except ValueError:
                pass  # AI analyzer is optional

    def analyze_stock(self, symbol: str, market: str = "us", 
                      period: str = "3mo", use_ai: bool = True) -> Dict:
        """
        Perform complete stock analysis
        
        Args:
            symbol: Stock symbol
            market: Market type (us, hk, cn)
            period: Analysis period
            use_ai: Whether to include AI analysis
            
        Returns:
            Complete analysis results
        """
        # Fetch stock data
        stock_data = self.data_fetcher.get_stock_data(symbol, market, period)
        
        # Perform technical analysis
        analyzer = TechnicalAnalyzer(stock_data["data"])
        technical_analysis = analyzer.get_full_analysis()
        
        # Add latest prices
        if stock_data["data"]:
            latest = stock_data["data"][-1]
            technical_analysis["latest_price"] = latest["close"]
            technical_analysis["latest_volume"] = latest["volume"]
            
            if len(stock_data["data"]) > 1:
                prev = stock_data["data"][-2]
                technical_analysis["price_change"] = latest["close"] - prev["close"]
                technical_analysis["price_change_percent"] = (
                    (latest["close"] - prev["close"]) / prev["close"] * 100
                )
        
        result = {
            "symbol": stock_data["symbol"],
            "market": market,
            "currency": stock_data.get("currency", "USD"),
            "current_price": stock_data.get("current_price"),
            "exchange": stock_data.get("exchange"),
            "market_state": stock_data.get("market_state"),
            "technical_analysis": technical_analysis,
            "data_points": len(stock_data["data"]),
            "period": period
        }
        
        # Add AI analysis if requested and available
        if use_ai and self.ai_analyzer:
            ai_result = self.ai_analyzer.analyze(stock_data, technical_analysis)
            result["ai_analysis"] = ai_result
        
        return result

    def search(self, query: str) -> List[Dict]:
        """
        Search for stocks
        
        Args:
            query: Search query
            
        Returns:
            List of matching stocks
        """
        return self.data_fetcher.search_stocks(query)

    def get_market_overview(self) -> Dict:
        """
        Get market overview with major indices
        
        Returns:
            Market summary dictionary
        """
        return self.data_fetcher.get_market_summary()

    def compare_stocks(self, symbols: List[str], market: str = "us", 
                       period: str = "3mo") -> Dict:
        """
        Compare multiple stocks
        
        Args:
            symbols: List of stock symbols
            market: Market type
            period: Analysis period
            
        Returns:
            Comparison results
        """
        comparisons = []
        
        for symbol in symbols:
            try:
                analysis = self.analyze_stock(symbol, market, period, use_ai=False)
                comparisons.append({
                    "symbol": analysis["symbol"],
                    "current_price": analysis["current_price"],
                    "currency": analysis["currency"],
                    "overall_signal": analysis["technical_analysis"]["overall_signal"],
                    "confidence": analysis["technical_analysis"]["confidence"],
                    "buy_signals": analysis["technical_analysis"]["buy_signals"],
                    "sell_signals": analysis["technical_analysis"]["sell_signals"]
                })
            except Exception as e:
                comparisons.append({
                    "symbol": symbol,
                    "error": str(e)
                })
        
        return {
            "market": market,
            "period": period,
            "comparisons": comparisons
        }

    def get_watchlist_summary(self, symbols: List[Dict]) -> Dict:
        """
        Get summary for a watchlist of stocks
        
        Args:
            symbols: List of dicts with 'symbol' and 'market' keys
            
        Returns:
            Watchlist summary
        """
        summaries = []
        
        for item in symbols:
            symbol = item.get("symbol")
            market = item.get("market", "us")
            
            try:
                stock_data = self.data_fetcher.get_stock_data(symbol, market, "5d")
                
                if stock_data["data"] and len(stock_data["data"]) >= 2:
                    latest = stock_data["data"][-1]
                    prev = stock_data["data"][-2]
                    
                    change = latest["close"] - prev["close"]
                    change_percent = (change / prev["close"]) * 100
                    
                    summaries.append({
                        "symbol": stock_data["symbol"],
                        "market": market,
                        "price": latest["close"],
                        "currency": stock_data.get("currency", "USD"),
                        "change": round(change, 2),
                        "change_percent": round(change_percent, 2),
                        "volume": latest["volume"]
                    })
            except Exception:
                continue
        
        return {
            "watchlist": summaries,
            "total": len(summaries),
            "gainers": sum(1 for s in summaries if s.get("change", 0) > 0),
            "losers": sum(1 for s in summaries if s.get("change", 0) < 0)
        }
