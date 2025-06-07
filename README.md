# Cryptocurrency Data Collector

A Python-based system for collecting and maintaining historical cryptocurrency price data using the Polygon.io API.

## Features

- Collects historical daily price data for multiple cryptocurrencies:
  - Bitcoin (BTCUSD)
  - Ethereum (ETHUSD)
  - Solana (SOLUSD)
  - Dogecoin (DOGEUSD)
  - Cardano (ADAUSD)
- Maintains separate CSV files for each cryptocurrency
- Implements rate limiting (12-second delay between API calls)
- Handles API errors and data validation
- Supports both historical data collection and daily updates

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/MohanP2005/data-collector.git
   cd data-collector
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create an `api_keys.txt` file in the root directory with your Polygon.io API key:
   ```
   POLYGON_API_KEY=your_api_key_here
   ```

## Usage

1. First-time setup - collect historical data:
   ```bash
   python src/daily_agg/historical_data_collector.py
   ```

2. Update with latest prices:
   ```bash
   python src/daily_agg/data_collector.py
   ```
