"""
Technical Analysis Module - Calculates various technical indicators

Implements common technical analysis indicators for stock evaluation
"""

from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from statistics import stdev


@dataclass
class IndicatorResult:
    """Result container for technical indicators"""
    name: str
    value: float
    signal: str  # "buy", "sell", "neutral"
    description: str


class TechnicalAnalyzer:
    """Technical analysis calculator for stock data"""

    def __init__(self, data: List[Dict]):
        """
        Initialize analyzer with stock data
        
        Args:
            data: List of OHLCV data dictionaries
        """
        self.data = sorted(data, key=lambda x: x.get("date", ""))
        self.closes = [d["close"] for d in self.data if "close" in d]
        self.highs = [d["high"] for d in self.data if "high" in d]
        self.lows = [d["low"] for d in self.data if "low" in d]
        self.volumes = [d["volume"] for d in self.data if "volume" in d]

    def calculate_ma(self, period: int = 20) -> List[float]:
        """
        Calculate Simple Moving Average (SMA)
        
        Args:
            period: Moving average period
            
        Returns:
            List of MA values
        """
        if len(self.closes) < period:
            return []
        
        ma = []
        for i in range(len(self.closes)):
            if i < period - 1:
                ma.append(None)
            else:
                ma.append(sum(self.closes[i-period+1:i+1]) / period)
        return ma

    def calculate_ema(self, period: int = 20) -> List[float]:
        """
        Calculate Exponential Moving Average (EMA)
        
        Args:
            period: EMA period
            
        Returns:
            List of EMA values
        """
        if len(self.closes) < period:
            return []
        
        multiplier = 2 / (period + 1)
        ema = [sum(self.closes[:period]) / period]  # Start with SMA
        
        for i in range(period, len(self.closes)):
            ema.append((self.closes[i] - ema[-1]) * multiplier + ema[-1])
        
        # Pad with None for the first (period-1) values
        return [None] * (period - 1) + ema

    def calculate_rsi(self, period: int = 14) -> List[float]:
        """
        Calculate Relative Strength Index (RSI)
        
        Args:
            period: RSI period
            
        Returns:
            List of RSI values (0-100)
        """
        if len(self.closes) < period + 1:
            return []
        
        gains = []
        losses = []
        
        # Calculate price changes
        for i in range(1, len(self.closes)):
            change = self.closes[i] - self.closes[i-1]
            gains.append(max(change, 0))
            losses.append(abs(min(change, 0)))
        
        rsi = [None] * period  # First 'period' values are None
        
        # Calculate initial averages
        avg_gain = sum(gains[:period]) / period
        avg_loss = sum(losses[:period]) / period
        
        for i in range(period, len(gains)):
            avg_gain = (avg_gain * (period - 1) + gains[i]) / period
            avg_loss = (avg_loss * (period - 1) + losses[i]) / period
            
            if avg_loss == 0:
                rsi.append(100)
            else:
                rs = avg_gain / avg_loss
                rsi.append(100 - (100 / (1 + rs)))
        
        return rsi

    def calculate_macd(self, fast: int = 12, slow: int = 26, signal: int = 9) -> Dict:
        """
        Calculate MACD (Moving Average Convergence Divergence)
        
        Args:
            fast: Fast EMA period
            slow: Slow EMA period
            signal: Signal line period
            
        Returns:
            Dictionary with MACD, Signal, and Histogram values
        """
        if len(self.closes) < slow:
            return {"macd": [], "signal": [], "histogram": []}
        
        ema_fast = self.calculate_ema(fast)
        ema_slow = self.calculate_ema(slow)
        
        # Calculate MACD line
        macd_line = []
        for i in range(len(self.closes)):
            if ema_fast[i] is None or ema_slow[i] is None:
                macd_line.append(None)
            else:
                macd_line.append(ema_fast[i] - ema_slow[i])
        
        # Calculate Signal line (EMA of MACD)
        valid_macd = [m for m in macd_line if m is not None]
        if len(valid_macd) < signal:
            return {"macd": macd_line, "signal": [], "histogram": []}
        
        multiplier = 2 / (signal + 1)
        signal_line = [sum(valid_macd[:signal]) / signal]
        
        for i in range(signal, len(valid_macd)):
            signal_line.append((valid_macd[i] - signal_line[-1]) * multiplier + signal_line[-1])
        
        # Pad signal line
        signal_line = [None] * (len(macd_line) - len(signal_line)) + signal_line
        
        # Calculate Histogram
        histogram = []
        for i in range(len(macd_line)):
            if macd_line[i] is not None and signal_line[i] is not None:
                histogram.append(macd_line[i] - signal_line[i])
            else:
                histogram.append(None)
        
        return {
            "macd": macd_line,
            "signal": signal_line,
            "histogram": histogram
        }

    def calculate_bollinger_bands(self, period: int = 20, std_dev: float = 2.0) -> Dict:
        """
        Calculate Bollinger Bands
        
        Args:
            period: Moving average period
            std_dev: Standard deviation multiplier
            
        Returns:
            Dictionary with upper, middle, and lower bands
        """
        if len(self.closes) < period:
            return {"upper": [], "middle": [], "lower": []}
        
        middle = self.calculate_ma(period)
        upper = []
        lower = []
        
        for i in range(len(self.closes)):
            if i < period - 1:
                upper.append(None)
                lower.append(None)
            else:
                std = stdev(self.closes[i-period+1:i+1])
                upper.append(middle[i] + (std * std_dev))
                lower.append(middle[i] - (std * std_dev))
        
        return {
            "upper": upper,
            "middle": middle,
            "lower": lower
        }

    def calculate_volume_ma(self, period: int = 20) -> List[float]:
        """Calculate Volume Moving Average"""
        if len(self.volumes) < period:
            return []
        
        vma = []
        for i in range(len(self.volumes)):
            if i < period - 1:
                vma.append(None)
            else:
                vma.append(sum(self.volumes[i-period+1:i+1]) / period)
        return vma

    def analyze_trend(self) -> IndicatorResult:
        """
        Analyze overall trend based on multiple indicators
        
        Returns:
            IndicatorResult with trend analysis
        """
        if len(self.closes) < 20:
            return IndicatorResult(
                name="Trend Analysis",
                value=0,
                signal="neutral",
                description="Insufficient data for trend analysis"
            )
        
        # Calculate indicators
        ma20 = self.calculate_ma(20)
        ma50 = self.calculate_ma(50) if len(self.closes) >= 50 else []
        
        current_price = self.closes[-1]
        current_ma20 = ma20[-1] if ma20[-1] is not None else 0
        current_ma50 = ma50[-1] if ma50 and ma50[-1] is not None else 0
        
        # Trend scoring
        score = 0
        signals = []
        
        # Price vs MA20
        if current_price > current_ma20:
            score += 1
            signals.append("Price above MA20")
        else:
            score -= 1
            signals.append("Price below MA20")
        
        # Price vs MA50
        if current_ma50 > 0:
            if current_price > current_ma50:
                score += 1
                signals.append("Price above MA50")
            else:
                score -= 1
                signals.append("Price below MA50")
        
        # MA20 vs MA50 (Golden/Death Cross)
        if len(ma50) > 0 and ma20[-1] is not None and ma50[-1] is not None:
            if ma20[-1] > ma50[-1]:
                score += 1
                signals.append("MA20 above MA50 (Bullish)")
            else:
                score -= 1
                signals.append("MA20 below MA50 (Bearish)")
        
        # Determine signal
        if score >= 2:
            signal = "buy"
        elif score <= -2:
            signal = "sell"
        else:
            signal = "neutral"
        
        return IndicatorResult(
            name="Trend Analysis",
            value=score,
            signal=signal,
            description="; ".join(signals)
        )

    def analyze_momentum(self) -> IndicatorResult:
        """
        Analyze momentum using RSI
        
        Returns:
            IndicatorResult with momentum analysis
        """
        rsi = self.calculate_rsi(14)
        
        if not rsi or rsi[-1] is None:
            return IndicatorResult(
                name="Momentum (RSI)",
                value=50,
                signal="neutral",
                description="Insufficient data for RSI calculation"
            )
        
        current_rsi = rsi[-1]
        
        if current_rsi > 70:
            signal = "sell"
            desc = f"RSI overbought ({current_rsi:.1f})"
        elif current_rsi < 30:
            signal = "buy"
            desc = f"RSI oversold ({current_rsi:.1f})"
        else:
            signal = "neutral"
            desc = f"RSI neutral ({current_rsi:.1f})"
        
        return IndicatorResult(
            name="Momentum (RSI)",
            value=current_rsi,
            signal=signal,
            description=desc
        )

    def analyze_volatility(self) -> IndicatorResult:
        """
        Analyze volatility using Bollinger Bands
        
        Returns:
            IndicatorResult with volatility analysis
        """
        bb = self.calculate_bollinger_bands()
        
        if not bb["middle"] or bb["middle"][-1] is None:
            return IndicatorResult(
                name="Volatility (Bollinger)",
                value=0,
                signal="neutral",
                description="Insufficient data for Bollinger Bands"
            )
        
        current_price = self.closes[-1]
        upper = bb["upper"][-1]
        lower = bb["lower"][-1]
        middle = bb["middle"][-1]
        
        if upper is None or lower is None:
            return IndicatorResult(
                name="Volatility (Bollinger)",
                value=0,
                signal="neutral",
                description="Bollinger Bands calculation error"
            )
        
        # Calculate bandwidth
        bandwidth = ((upper - lower) / middle) * 100
        
        # Determine position within bands
        if current_price > upper:
            signal = "sell"
            desc = f"Price above upper band, potential reversal ({bandwidth:.1f}% bandwidth)"
        elif current_price < lower:
            signal = "buy"
            desc = f"Price below lower band, potential bounce ({bandwidth:.1f}% bandwidth)"
        else:
            signal = "neutral"
            desc = f"Price within bands ({bandwidth:.1f}% bandwidth)"
        
        return IndicatorResult(
            name="Volatility (Bollinger)",
            value=bandwidth,
            signal=signal,
            description=desc
        )

    def analyze_macd_signal(self) -> IndicatorResult:
        """
        Analyze MACD signals
        
        Returns:
            IndicatorResult with MACD analysis
        """
        macd_data = self.calculate_macd()
        
        if not macd_data["macd"] or macd_data["macd"][-1] is None:
            return IndicatorResult(
                name="MACD",
                value=0,
                signal="neutral",
                description="Insufficient data for MACD calculation"
            )
        
        macd_line = macd_data["macd"]
        signal_line = macd_data["signal"]
        
        if len(macd_line) < 2 or signal_line[-1] is None:
            return IndicatorResult(
                name="MACD",
                value=macd_line[-1] if macd_line[-1] is not None else 0,
                signal="neutral",
                description="Waiting for signal line"
            )
        
        current_macd = macd_line[-1]
        current_signal = signal_line[-1]
        prev_macd = macd_line[-2] if len(macd_line) > 1 and macd_line[-2] is not None else current_macd
        prev_signal = signal_line[-2] if len(signal_line) > 1 and signal_line[-2] is not None else current_signal
        
        # Detect crossover
        if prev_macd < prev_signal and current_macd > current_signal:
            signal = "buy"
            desc = "MACD bullish crossover"
        elif prev_macd > prev_signal and current_macd < current_signal:
            signal = "sell"
            desc = "MACD bearish crossover"
        elif current_macd > current_signal:
            signal = "neutral"
            desc = "MACD above signal (bullish)"
        else:
            signal = "neutral"
            desc = "MACD below signal (bearish)"
        
        return IndicatorResult(
            name="MACD",
            value=current_macd,
            signal=signal,
            description=desc
        )

    def get_full_analysis(self) -> Dict:
        """
        Get complete technical analysis
        
        Returns:
            Dictionary with all indicators and overall recommendation
        """
        trend = self.analyze_trend()
        momentum = self.analyze_momentum()
        volatility = self.analyze_volatility()
        macd = self.analyze_macd_signal()
        
        indicators = [trend, momentum, volatility, macd]
        
        # Calculate overall signal
        buy_count = sum(1 for i in indicators if i.signal == "buy")
        sell_count = sum(1 for i in indicators if i.signal == "sell")
        
        if buy_count >= 2:
            overall_signal = "buy"
        elif sell_count >= 2:
            overall_signal = "sell"
        else:
            overall_signal = "neutral"
        
        # Calculate confidence (0-100)
        max_possible = len(indicators)
        confidence = max(buy_count, sell_count) / max_possible * 100
        
        return {
            "indicators": indicators,
            "overall_signal": overall_signal,
            "confidence": round(confidence, 1),
            "buy_signals": buy_count,
            "sell_signals": sell_count,
            "neutral_signals": len(indicators) - buy_count - sell_count
        }
