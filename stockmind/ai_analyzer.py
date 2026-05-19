"""
AI Analysis Module - Integrates with LLM APIs for intelligent stock insights

Supports multiple LLM providers for AI-powered stock analysis
"""

import json
import os
from typing import Dict, List, Optional
from dataclasses import asdict
import requests


class AIAnalyzer:
    """AI-powered stock analysis using LLM APIs"""

    SUPPORTED_PROVIDERS = ["openai", "anthropic", "deepseek", "glm"]

    def __init__(self, provider: str = "openai", api_key: Optional[str] = None):
        """
        Initialize AI analyzer
        
        Args:
            provider: LLM provider (openai, anthropic, deepseek, glm)
            api_key: API key for the provider (falls back to env var)
        """
        self.provider = provider.lower()
        if self.provider not in self.SUPPORTED_PROVIDERS:
            raise ValueError(f"Unsupported provider: {provider}. Use: {self.SUPPORTED_PROVIDERS}")
        
        # Get API key from parameter or environment
        env_var_map = {
            "openai": "OPENAI_API_KEY",
            "anthropic": "ANTHROPIC_API_KEY",
            "deepseek": "DEEPSEEK_API_KEY",
            "glm": "GLM_API_KEY"
        }
        
        self.api_key = api_key or os.getenv(env_var_map.get(self.provider))
        self.session = requests.Session()

    def _build_prompt(self, stock_data: Dict, technical_analysis: Dict) -> str:
        """
        Build analysis prompt for LLM
        
        Args:
            stock_data: Stock data dictionary
            technical_analysis: Technical analysis results
            
        Returns:
            Formatted prompt string
        """
        symbol = stock_data.get("symbol", "Unknown")
        current_price = stock_data.get("current_price", "N/A")
        currency = stock_data.get("currency", "USD")
        
        # Get recent price history
        data_points = stock_data.get("data", [])
        recent_prices = data_points[-10:] if len(data_points) >= 10 else data_points
        
        price_history = "\n".join([
            f"  {d['date']}: Open={d['open']}, High={d['high']}, Low={d['low']}, Close={d['close']}, Vol={d['volume']}"
            for d in recent_prices
        ])
        
        # Technical indicators summary
        indicators = technical_analysis.get("indicators", [])
        indicator_summary = "\n".join([
            f"  - {i.name}: {i.signal.upper()} (Value: {i.value:.2f}) - {i.description}"
            for i in indicators
        ])
        
        prompt = f"""You are a professional stock analyst. Analyze the following stock data and provide investment insights.

Stock Information:
- Symbol: {symbol}
- Current Price: {current_price} {currency}
- Exchange: {stock_data.get("exchange", "Unknown")}

Recent Price History (Last {len(recent_prices)} days):
{price_history}

Technical Analysis Results:
{indicator_summary}

Overall Signal: {technical_analysis.get("overall_signal", "neutral").upper()}
Confidence: {technical_analysis.get("confidence", 0)}%

Please provide:
1. A brief summary of the current market condition (2-3 sentences)
2. Key support and resistance levels based on the data
3. Potential risks and opportunities
4. Short-term outlook (1-4 weeks)
5. One actionable recommendation (Buy/Hold/Sell with brief reasoning)

Keep your analysis concise, professional, and data-driven."""

        return prompt

    def _call_openai(self, prompt: str) -> str:
        """Call OpenAI API"""
        if not self.api_key:
            return "Error: OpenAI API key not configured"
        
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are a professional stock market analyst."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 800
        }
        
        try:
            response = self.session.post(url, headers=headers, json=data, timeout=60)
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except requests.RequestException as e:
            return f"Error calling OpenAI API: {str(e)}"
        except (KeyError, IndexError) as e:
            return f"Error parsing OpenAI response: {str(e)}"

    def _call_anthropic(self, prompt: str) -> str:
        """Call Anthropic Claude API"""
        if not self.api_key:
            return "Error: Anthropic API key not configured"
        
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        data = {
            "model": "claude-3-haiku-20240307",
            "max_tokens": 800,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        
        try:
            response = self.session.post(url, headers=headers, json=data, timeout=60)
            response.raise_for_status()
            result = response.json()
            return result["content"][0]["text"]
        except requests.RequestException as e:
            return f"Error calling Anthropic API: {str(e)}"
        except (KeyError, IndexError) as e:
            return f"Error parsing Anthropic response: {str(e)}"

    def _call_deepseek(self, prompt: str) -> str:
        """Call DeepSeek API"""
        if not self.api_key:
            return "Error: DeepSeek API key not configured"
        
        url = "https://api.deepseek.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "You are a professional stock market analyst."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 800
        }
        
        try:
            response = self.session.post(url, headers=headers, json=data, timeout=60)
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except requests.RequestException as e:
            return f"Error calling DeepSeek API: {str(e)}"
        except (KeyError, IndexError) as e:
            return f"Error parsing DeepSeek response: {str(e)}"

    def _call_glm(self, prompt: str) -> str:
        """Call GLM (Zhipu AI) API"""
        if not self.api_key:
            return "Error: GLM API key not configured"
        
        url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "glm-4-flash",
            "messages": [
                {"role": "system", "content": "You are a professional stock market analyst."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 800
        }
        
        try:
            response = self.session.post(url, headers=headers, json=data, timeout=60)
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except requests.RequestException as e:
            return f"Error calling GLM API: {str(e)}"
        except (KeyError, IndexError) as e:
            return f"Error parsing GLM response: {str(e)}"

    def analyze(self, stock_data: Dict, technical_analysis: Dict) -> Dict:
        """
        Perform AI analysis on stock data
        
        Args:
            stock_data: Stock data dictionary
            technical_analysis: Technical analysis results
            
        Returns:
            Dictionary with AI analysis results
        """
        prompt = self._build_prompt(stock_data, technical_analysis)
        
        # Call appropriate API
        api_methods = {
            "openai": self._call_openai,
            "anthropic": self._call_anthropic,
            "deepseek": self._call_deepseek,
            "glm": self._call_glm
        }
        
        analysis_text = api_methods[self.provider](prompt)
        
        # Check if there was an error
        if analysis_text.startswith("Error:"):
            return {
                "success": False,
                "error": analysis_text,
                "analysis": None,
                "provider": self.provider
            }
        
        return {
            "success": True,
            "error": None,
            "analysis": analysis_text,
            "provider": self.provider
        }

    def get_quick_insight(self, symbol: str, current_price: float, 
                          change_percent: float) -> str:
        """
        Get a quick AI insight for a stock
        
        Args:
            symbol: Stock symbol
            current_price: Current price
            change_percent: Price change percentage
            
        Returns:
            Quick insight string
        """
        prompt = f"""Provide a one-sentence market insight for {symbol} currently trading at {current_price} ({change_percent:+.2f}% today).

Keep it brief, professional, and actionable."""

        api_methods = {
            "openai": self._call_openai,
            "anthropic": self._call_anthropic,
            "deepseek": self._call_deepseek,
            "glm": self._call_glm
        }
        
        result = api_methods[self.provider](prompt)
        
        if result.startswith("Error:"):
            return f"AI insight unavailable: {result}"
        
        return result
