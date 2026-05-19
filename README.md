# 📈 StockMind - AI驱动的股票分析CLI工具

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)]()

**简体中文** | [繁體中文](#繁體中文) | [English](#english)

</div>

---

## 🎉 项目介绍

**StockMind** 是一款轻量级、智能化的股票分析CLI工具，专为投资者和交易者设计。它结合了传统技术分析指标与AI智能洞察，支持美股、港股和A股三大市场，帮助您做出更明智的投资决策。

### 💡 灵感来源

本项目灵感来源于 GitHub Trending 上的热门项目 [daily_stock_analysis](https://github.com/ZhuLinsen/daily_stock_analysis)，我们在此基础上进行了**完全独立自研开发**，专注于打造更轻量、更易用的命令行工具。

### ✨ 自研差异化亮点

- 🚀 **纯Python实现** - 单文件依赖（仅requests），零配置即可运行
- 🌍 **多市场支持** - 美股、港股、A股全覆盖
- 🤖 **AI智能分析** - 支持OpenAI、Anthropic、DeepSeek、GLM等多种LLM
- 📊 **完整技术指标** - MA、RSI、MACD、布林带等经典指标
- 💾 **智能缓存系统** - 本地缓存机制，减少API调用，提升响应速度
- 🎨 **精美CLI界面** - 丰富的表情符号和格式化输出

---

## ✨ 核心特性

### 📐 技术分析指标
- **移动平均线 (MA)** - 支持SMA和EMA计算
- **相对强弱指数 (RSI)** - 识别超买超卖信号
- **MACD指标** - 趋势跟踪和动量分析
- **布林带 (Bollinger Bands)** - 波动率分析和价格通道

### 🤖 AI智能分析
- 支持 **OpenAI GPT** 系列模型
- 支持 **Anthropic Claude** 系列模型
- 支持 **DeepSeek** 大模型
- 支持 **智谱GLM** 系列模型

### 🌍 多市场支持
| 市场 | 代码示例 | 说明 |
|------|---------|------|
| 美股 | `AAPL`, `TSLA`, `MSFT` | 美国上市公司 |
| 港股 | `0700.HK`, `9988.HK` | 香港交易所 |
| A股 | `000001.SZ`, `600000.SS` | 沪深股市 |

### 📊 实用功能
- 🔍 **股票搜索** - 快速查找股票代码
- 📈 **个股分析** - 完整的技术分析+AI洞察
- 🔄 **多股对比** - 横向比较多只股票
- ⭐ **自选股监控** - 实时监控关注股票
- 🌍 **市场概览** - 全球主要指数行情

---

## 🚀 快速开始

### 环境要求
- **Python**: 3.8 或更高版本
- **操作系统**: Windows / macOS / Linux

### 安装步骤

#### 方式一：通过 pip 安装（推荐）

```bash
pip install stockmind
```

#### 方式二：从源码安装

```bash
git clone https://github.com/gitstq/stockmind.git
cd stockmind
pip install -e .
```

#### 方式三：直接运行（无需安装）

```bash
git clone https://github.com/gitstq/stockmind.git
cd stockmind
pip install -r requirements.txt
python -m stockmind.cli analyze AAPL
```

### 配置AI分析（可选）

如需使用AI分析功能，请设置环境变量：

```bash
# OpenAI
export OPENAI_API_KEY="your-openai-api-key"

# Anthropic Claude
export ANTHROPIC_API_KEY="your-anthropic-api-key"

# DeepSeek
export DEEPSEEK_API_KEY="your-deepseek-api-key"

# 智谱GLM
export GLM_API_KEY="your-glm-api-key"

# 设置默认AI提供商
export STOCKMIND_AI_PROVIDER="openai"  # 可选: openai, anthropic, deepseek, glm
```

---

## 📖 详细使用指南

### 1️⃣ 分析单只股票

```bash
# 分析美股（默认）
stockmind analyze AAPL

# 分析港股
stockmind analyze 0700.HK --market hk

# 分析A股
stockmind analyze 000001.SZ --market cn

# 指定分析周期
stockmind analyze AAPL --period 6mo  # 可选: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y

# 禁用AI分析
stockmind analyze AAPL --no-ai

# 指定AI提供商
stockmind analyze AAPL --ai-provider deepseek

# 输出JSON格式
stockmind analyze AAPL -o analysis.json
```

### 2️⃣ 搜索股票

```bash
# 搜索苹果相关股票
stockmind search apple

# 搜索腾讯
stockmind search tencent
```

### 3️⃣ 查看市场概览

```bash
# 显示全球主要指数
stockmind market
```

### 4️⃣ 多股对比

```bash
# 对比多只美股
stockmind compare AAPL MSFT GOOGL

# 对比港股
stockmind compare 0700.HK 9988.HK --market hk

# 指定分析周期
stockmind compare AAPL TSLA NVDA --period 1mo
```

### 5️⃣ 自选股监控

```bash
# 监控多只股票
stockmind watchlist AAPL MSFT TSLA

# 监控港股
stockmind watchlist 0700.HK 9988.HK --market hk
```

---

## 💡 设计思路与迭代规划

### 🎯 设计理念

StockMind 的设计理念是**"简洁而不简单"**。我们相信，优秀的工具应该：
- ✅ 开箱即用，无需复杂配置
- ✅ 功能专注，解决核心问题
- ✅ 输出清晰，一目了然
- ✅ 扩展灵活，支持个性化需求

### 🔧 技术选型原因

| 技术 | 选型原因 |
|------|---------|
| **Python** | 生态丰富，金融分析库完善 |
| **Yahoo Finance API** | 免费、稳定、覆盖全球市场 |
| **Requests** | 轻量级HTTP库，满足基本需求 |
| **多LLM支持** | 给用户更多选择，避免 vendor lock-in |

### 📅 后续迭代计划

#### v1.1.0（计划中）
- [ ] 支持更多技术指标（KDJ、CCI、威廉指标）
- [ ] 添加图表生成功能
- [ ] 支持自定义扫描策略

#### v1.2.0（计划中）
- [ ] 添加回测功能
- [ ] 支持邮件/微信推送
- [ ] 添加投资组合分析

#### v2.0.0（远期规划）
- [ ] Web界面版本
- [ ] 实时数据流支持
- [ ] 机器学习预测模型

### 🤝 社区贡献方向

我们欢迎以下方面的贡献：
- 🐛 **Bug修复** - 报告和修复问题
- ✨ **新功能** - 添加新的技术指标或数据源
- 🌍 **本地化** - 添加更多语言支持
- 📚 **文档** - 完善使用文档和教程

---

## 📦 打包与部署

### 打包为可执行文件

#### 使用 PyInstaller

```bash
# 安装 PyInstaller
pip install pyinstaller

# 打包为单文件可执行程序
pyinstaller --onefile --name stockmind stockmind/cli.py

# 打包后的文件位于 dist/ 目录
dist/stockmind
```

#### 使用 cx_Freeze

```bash
# 安装 cx_Freeze
pip install cx_freeze

# 创建 setup.py 构建配置
python setup.py build

# 打包后的文件位于 build/ 目录
```

### 发布到 PyPI

```bash
# 安装构建工具
pip install build twine

# 构建包
python -m build

# 上传到 PyPI
python -m twine upload dist/*
```

---

## 🤝 贡献指南

### 提交PR

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'feat: add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

### 提交规范

我们使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

- `feat:` 新功能
- `fix:` Bug修复
- `docs:` 文档更新
- `style:` 代码格式调整
- `refactor:` 代码重构
- `test:` 测试相关
- `chore:` 构建/工具相关

### Issue反馈

提交Issue时请包含：
- 问题描述
- 复现步骤
- 期望行为
- 实际行为
- 环境信息（Python版本、操作系统）

---

## 📄 开源协议

本项目采用 [MIT License](LICENSE) 开源协议。

```
MIT License

Copyright (c) 2025 StockMind Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## ⚠️ 免责声明

**投资有风险，入市需谨慎。**

StockMind 提供的分析结果仅供参考，不构成任何投资建议。投资者应根据自身情况独立做出投资决策，并自行承担投资风险。

- 历史数据不代表未来表现
- 技术分析存在局限性
- AI分析可能存在偏差
- 请理性投资，量力而行

---

<div align="center">

**Made with ❤️ by StockMind Team**

⭐ 如果这个项目对您有帮助，请给我们一个 Star！

</div>

---

# 繁體中文

## 🎉 項目介紹

**StockMind** 是一款輕量級、智能化的股票分析CLI工具，專為投資者和交易者設計。它結合了傳統技術分析指標與AI智能洞察，支持美股、港股和A股三大市場。

### ✨ 核心特性

- 📐 **完整技術指標** - MA、RSI、MACD、布林帶
- 🤖 **AI智能分析** - 支持多種LLM提供商
- 🌍 **多市場支持** - 美股、港股、A股
- 💾 **智能緩存** - 提升響應速度
- 🎨 **精美界面** - 豐富的表情符號

### 🚀 快速開始

```bash
# 安裝
pip install stockmind

# 分析股票
stockmind analyze AAPL

# 搜索股票
stockmind search apple

# 市場概覽
stockmind market
```

---

# English

## 🎉 Introduction

**StockMind** is a lightweight, intelligent stock analysis CLI tool designed for investors and traders. It combines traditional technical analysis indicators with AI-powered insights, supporting US, Hong Kong, and China A-share markets.

### ✨ Key Features

- 📐 **Complete Technical Indicators** - MA, RSI, MACD, Bollinger Bands
- 🤖 **AI-Powered Analysis** - Multiple LLM provider support
- 🌍 **Multi-Market Support** - US, HK, China A-shares
- 💾 **Smart Caching** - Improved response speed
- 🎨 **Beautiful Interface** - Rich emoji and formatting

### 🚀 Quick Start

```bash
# Install
pip install stockmind

# Analyze stock
stockmind analyze AAPL

# Search stocks
stockmind search apple

# Market overview
stockmind market
```

### 📊 Supported Markets

| Market | Examples | Description |
|--------|----------|-------------|
| US | `AAPL`, `TSLA`, `MSFT` | US Listed Companies |
| HK | `0700.HK`, `9988.HK` | Hong Kong Exchange |
| CN | `000001.SZ`, `600000.SS` | Shanghai/Shenzhen |

### 🤖 AI Providers

- OpenAI GPT series
- Anthropic Claude series
- DeepSeek
- Zhipu GLM series

---

<div align="center">

**[⬆ Back to Top](#-stockmind---ai驱动的股票分析cli工具)**

</div>
