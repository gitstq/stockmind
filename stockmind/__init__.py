"""
StockMind - AI-Powered Stock Analysis CLI Tool

A lightweight, intelligent stock analysis tool that combines technical indicators
with AI-powered insights for A-shares, Hong Kong stocks, and US stocks.

Author: StockMind Team
Version: 1.0.0
License: MIT
"""

__version__ = "1.0.0"
__author__ = "StockMind Team"
__license__ = "MIT"

from .core import StockMind
from .analyzer import TechnicalAnalyzer
from .data_fetcher import DataFetcher

__all__ = ["StockMind", "TechnicalAnalyzer", "DataFetcher"]
