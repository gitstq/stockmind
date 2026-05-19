"""
StockMind - AI-Powered Stock Analysis CLI Tool
Setup configuration
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

setup(
    name="stockmind",
    version="1.0.0",
    author="StockMind Team",
    author_email="contact@stockmind.dev",
    description="AI-Powered Stock Analysis CLI Tool - Technical Analysis meets AI Insights",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lobster959/stockmind",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.28.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "stockmind=stockmind.cli:main",
        ],
    },
    keywords="stock analysis trading technical-analysis ai finance investment cli",
    project_urls={
        "Bug Reports": "https://github.com/lobster959/stockmind/issues",
        "Source": "https://github.com/lobster959/stockmind",
        "Documentation": "https://github.com/lobster959/stockmind#readme",
    },
)
