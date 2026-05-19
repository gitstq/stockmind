"""
CLI Module - Command-line interface for StockMind

Provides interactive and command-line interface for stock analysis
"""

import argparse
import json
import os
import sys
from typing import Optional

from .core import StockMind
from . import __version__


def print_banner():
    """Print application banner"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   📈 StockMind v{} - AI-Powered Stock Analysis CLI      ║
║                                                              ║
║   Technical Analysis + AI Insights for Smarter Trading      ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""".format(__version__)
    print(banner)


def format_price(price: float, currency: str = "USD") -> str:
    """Format price with currency"""
    if currency == "CNY":
        return f"¥{price:,.2f}"
    elif currency == "HKD":
        return f"HK${price:,.2f}"
    else:
        return f"${price:,.2f}"


def print_analysis(result: dict, show_ai: bool = True):
    """Print formatted analysis results"""
    print("\n" + "=" * 60)
    print(f"📊 股票分析结果 | Stock Analysis Results")
    print("=" * 60)
    
    # Basic Info
    symbol = result.get("symbol", "N/A")
    market = result.get("market", "us").upper()
    currency = result.get("currency", "USD")
    
    print(f"\n🏷️  股票代码 (Symbol): {symbol}")
    print(f"🌏 市场 (Market): {market}")
    print(f"💱 货币 (Currency): {currency}")
    
    # Price Info
    current_price = result.get("current_price")
    if current_price:
        print(f"\n💰 当前价格 (Current Price): {format_price(current_price, currency)}")
    
    tech = result.get("technical_analysis", {})
    
    if "latest_price" in tech:
        print(f"📈 最新收盘价 (Latest Close): {format_price(tech['latest_price'], currency)}")
    
    if "price_change" in tech and "price_change_percent" in tech:
        change = tech["price_change"]
        change_pct = tech["price_change_percent"]
        emoji = "🟢" if change >= 0 else "🔴"
        print(f"{emoji} 涨跌 (Change): {change:+.2f} ({change_pct:+.2f}%)")
    
    if "latest_volume" in tech:
        print(f"📊 成交量 (Volume): {tech['latest_volume']:,}")
    
    # Technical Analysis Summary
    print("\n" + "-" * 60)
    print("📐 技术分析指标 (Technical Indicators)")
    print("-" * 60)
    
    indicators = tech.get("indicators", [])
    for indicator in indicators:
        signal = indicator.get("signal", "neutral")
        signal_emoji = {"buy": "🟢 买入", "sell": "🔴 卖出", "neutral": "⚪ 中性"}.get(signal, "⚪")
        
        print(f"\n🔹 {indicator.get('name', 'Unknown')}")
        print(f"   信号 (Signal): {signal_emoji}")
        print(f"   数值 (Value): {indicator.get('value', 0):.2f}")
        print(f"   说明 (Description): {indicator.get('description', 'N/A')}")
    
    # Overall Signal
    print("\n" + "=" * 60)
    overall = tech.get("overall_signal", "neutral")
    confidence = tech.get("confidence", 0)
    
    signal_map = {
        "buy": ("🟢 买入信号 (BUY)", "建议考虑买入"),
        "sell": ("🔴 卖出信号 (SELL)", "建议考虑卖出"),
        "neutral": ("⚪ 中性信号 (NEUTRAL)", "建议观望")
    }
    
    signal_text, signal_advice = signal_map.get(overall, ("⚪ 未知", ""))
    print(f"📋 综合信号 (Overall Signal): {signal_text}")
    print(f"🎯 置信度 (Confidence): {confidence}%")
    print(f"💡 建议 (Advice): {signal_advice}")
    
    # Signal counts
    buy_count = tech.get("buy_signals", 0)
    sell_count = tech.get("sell_signals", 0)
    neutral_count = tech.get("neutral_signals", 0)
    
    print(f"\n📊 指标统计:")
    print(f"   🟢 买入指标: {buy_count}")
    print(f"   🔴 卖出指标: {sell_count}")
    print(f"   ⚪ 中性指标: {neutral_count}")
    
    # AI Analysis
    if show_ai and "ai_analysis" in result:
        ai = result["ai_analysis"]
        print("\n" + "=" * 60)
        print("🤖 AI 智能分析 (AI Analysis)")
        print("=" * 60)
        
        if ai.get("success"):
            print(f"\n提供商 (Provider): {ai.get('provider', 'Unknown').upper()}")
            print(f"\n{ai.get('analysis', 'No analysis available')}")
        else:
            print(f"\n⚠️ AI分析不可用: {ai.get('error', 'Unknown error')}")
    
    print("\n" + "=" * 60)
    print("⚠️ 免责声明: 本分析仅供参考，不构成投资建议")
    print("   Disclaimer: This analysis is for reference only and does not constitute investment advice.")
    print("=" * 60 + "\n")


def print_market_overview(overview: dict):
    """Print market overview"""
    print("\n" + "=" * 60)
    print("🌍 全球市场概览 (Global Market Overview)")
    print("=" * 60 + "\n")
    
    for name, data in overview.items():
        price = data.get("price", 0)
        change = data.get("change", 0)
        change_pct = data.get("change_percent", 0)
        
        emoji = "🟢" if change >= 0 else "🔴"
        
        print(f"{emoji} {name}")
        print(f"   指数: {price:,.2f}")
        print(f"   涨跌: {change:+.2f} ({change_pct:+.2f}%)")
        print()
    
    print("=" * 60 + "\n")


def print_comparison(comparison: dict):
    """Print stock comparison results"""
    print("\n" + "=" * 60)
    print("📊 股票对比分析 (Stock Comparison)")
    print("=" * 60)
    
    market = comparison.get("market", "us").upper()
    period = comparison.get("period", "3mo")
    
    print(f"\n市场 (Market): {market}")
    print(f"周期 (Period): {period}\n")
    
    comparisons = comparison.get("comparisons", [])
    
    # Header
    print(f"{'Symbol':<12} {'Price':<15} {'Signal':<12} {'Confidence':<12} {'B/S/N':<10}")
    print("-" * 60)
    
    for comp in comparisons:
        if "error" in comp:
            print(f"{comp['symbol']:<12} Error: {comp['error'][:30]}")
            continue
        
        symbol = comp.get("symbol", "N/A")
        price = comp.get("current_price", 0)
        currency = comp.get("currency", "USD")
        signal = comp.get("overall_signal", "neutral").upper()
        confidence = comp.get("confidence", 0)
        buy = comp.get("buy_signals", 0)
        sell = comp.get("sell_signals", 0)
        neutral = 4 - buy - sell
        
        price_str = format_price(price, currency) if price else "N/A"
        signal_emoji = {"BUY": "🟢", "SELL": "🔴", "NEUTRAL": "⚪"}.get(signal, "⚪")
        
        print(f"{symbol:<12} {price_str:<15} {signal_emoji} {signal:<10} {confidence:>5}%      {buy}/{sell}/{neutral}")
    
    print("\n" + "=" * 60)
    print("图例 (Legend): B/S/N = Buy/Sell/Neutral signals count")
    print("=" * 60 + "\n")


def print_watchlist(watchlist: dict):
    """Print watchlist summary"""
    print("\n" + "=" * 60)
    print("⭐ 自选股监控 (Watchlist)")
    print("=" * 60 + "\n")
    
    items = watchlist.get("watchlist", [])
    total = watchlist.get("total", 0)
    gainers = watchlist.get("gainers", 0)
    losers = watchlist.get("losers", 0)
    
    print(f"总计 (Total): {total} | 🟢 上涨 (Up): {gainers} | 🔴 下跌 (Down): {losers}\n")
    
    if items:
        print(f"{'Symbol':<12} {'Market':<8} {'Price':<15} {'Change':<15} {'Volume':<15}")
        print("-" * 60)
        
        for item in items:
            symbol = item.get("symbol", "N/A")
            market = item.get("market", "us").upper()
            price = item.get("price", 0)
            currency = item.get("currency", "USD")
            change = item.get("change", 0)
            change_pct = item.get("change_percent", 0)
            volume = item.get("volume", 0)
            
            price_str = format_price(price, currency)
            change_str = f"{change:+.2f} ({change_pct:+.2f}%)"
            emoji = "🟢" if change >= 0 else "🔴"
            
            print(f"{symbol:<12} {market:<8} {price_str:<15} {emoji} {change_str:<13} {volume:>12,}")
    
    print("\n" + "=" * 60 + "\n")


def print_search_results(results: list, query: str):
    """Print search results"""
    print("\n" + "=" * 60)
    print(f"🔍 搜索结果 (Search Results): '{query}'")
    print("=" * 60 + "\n")
    
    if not results:
        print("未找到匹配的股票 (No matching stocks found).\n")
        return
    
    print(f"{'Symbol':<12} {'Name':<30} {'Exchange':<15} {'Type':<10}")
    print("-" * 60)
    
    for result in results[:10]:  # Show top 10
        symbol = result.get("symbol", "N/A")
        name = result.get("name", "N/A")[:28]
        exchange = result.get("exchange", "N/A")
        type_ = result.get("type", "N/A")
        
        print(f"{symbol:<12} {name:<30} {exchange:<15} {type_:<10}")
    
    print(f"\n共找到 {len(results)} 个结果 (Total {len(results)} results found)")
    print("=" * 60 + "\n")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="StockMind - AI-Powered Stock Analysis CLI Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s analyze AAPL                    # Analyze Apple stock
  %(prog)s analyze 0700.HK --market hk     # Analyze Tencent
  %(prog)s analyze 000001.SZ --market cn   # Analyze Ping An Bank
  %(prog)s search apple                    # Search for Apple
  %(prog)s market                          # Show market overview
  %(prog)s compare AAPL MSFT GOOGL         # Compare multiple stocks
        """
    )
    
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("--no-ai", action="store_true", help="Disable AI analysis")
    parser.add_argument("--ai-provider", choices=["openai", "anthropic", "deepseek", "glm"],
                       help="AI provider for analysis")
    parser.add_argument("--cache-dir", default=".stockmind_cache", help="Cache directory")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Analyze command
    analyze_parser = subparsers.add_parser("analyze", help="Analyze a stock")
    analyze_parser.add_argument("symbol", help="Stock symbol (e.g., AAPL, 0700.HK)")
    analyze_parser.add_argument("--market", choices=["us", "hk", "cn"], default="us",
                               help="Market type (default: us)")
    analyze_parser.add_argument("--period", default="3mo",
                               choices=["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y"],
                               help="Analysis period (default: 3mo)")
    analyze_parser.add_argument("--output", "-o", help="Output file (JSON format)")
    
    # Search command
    search_parser = subparsers.add_parser("search", help="Search for stocks")
    search_parser.add_argument("query", help="Search query")
    
    # Market command
    subparsers.add_parser("market", help="Show market overview")
    
    # Compare command
    compare_parser = subparsers.add_parser("compare", help="Compare multiple stocks")
    compare_parser.add_argument("symbols", nargs="+", help="Stock symbols to compare")
    compare_parser.add_argument("--market", choices=["us", "hk", "cn"], default="us")
    compare_parser.add_argument("--period", default="3mo",
                               choices=["1d", "5d", "1mo", "3mo", "6mo", "1y"])
    
    # Watchlist command
    watchlist_parser = subparsers.add_parser("watchlist", help="Monitor watchlist")
    watchlist_parser.add_argument("symbols", nargs="+", help="Stock symbols to monitor")
    watchlist_parser.add_argument("--market", choices=["us", "hk", "cn"], default="us")
    
    args = parser.parse_args()
    
    # Print banner
    print_banner()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Initialize StockMind
    ai_provider = args.ai_provider or os.getenv("STOCKMIND_AI_PROVIDER")
    ai_api_key = None
    
    if ai_provider:
        key_map = {
            "openai": "OPENAI_API_KEY",
            "anthropic": "ANTHROPIC_API_KEY",
            "deepseek": "DEEPSEEK_API_KEY",
            "glm": "GLM_API_KEY"
        }
        ai_api_key = os.getenv(key_map.get(ai_provider))
    
    try:
        stockmind = StockMind(
            cache_dir=args.cache_dir,
            ai_provider=ai_provider,
            ai_api_key=ai_api_key
        )
    except Exception as e:
        print(f"Error initializing StockMind: {e}")
        sys.exit(1)
    
    # Execute command
    try:
        if args.command == "analyze":
            print(f"🔍 Analyzing {args.symbol} ({args.market.upper()})...")
            result = stockmind.analyze_stock(
                args.symbol, 
                args.market, 
                args.period,
                use_ai=not args.no_ai
            )
            
            if args.output:
                with open(args.output, "w", encoding="utf-8") as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)
                print(f"✅ Results saved to {args.output}")
            
            print_analysis(result, show_ai=not args.no_ai)
            
        elif args.command == "search":
            results = stockmind.search(args.query)
            print_search_results(results, args.query)
            
        elif args.command == "market":
            overview = stockmind.get_market_overview()
            print_market_overview(overview)
            
        elif args.command == "compare":
            comparison = stockmind.compare_stocks(args.symbols, args.market, args.period)
            print_comparison(comparison)
            
        elif args.command == "watchlist":
            symbols = [{"symbol": s, "market": args.market} for s in args.symbols]
            watchlist = stockmind.get_watchlist_summary(symbols)
            print_watchlist(watchlist)
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
