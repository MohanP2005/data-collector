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
