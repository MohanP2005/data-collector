import requests
import os
import pandas as pd
from datetime import datetime, timedelta
import time

# List of cryptocurrencies to track
CRYPTO_PAIRS = [
    "X:BTCUSD",  # Bitcoin
    "X:ETHUSD",  # Ethereum
    "X:SOLUSD",  # Solana
    "X:DOGEUSD", # Dogecoin
    "X:ADAUSD",  # Cardano
]

def read_api_key(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('POLYGON_API_KEY'):
                parts = [part.strip() for part in line.split('=', 1)]
                if len(parts) == 2:
                    return parts[1]
    raise ValueError("POLYGON_API_KEY not found in api_keys.txt")

def get_polygon_data(api_key, ticker, start_date, end_date):
    url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{start_date}/{end_date}?adjusted=true&sort=asc&limit=5000&apiKey={api_key}"
    response = requests.get(url)
    data = response.json()
    
    if "results" not in data or not data["results"]:
        print(f"No data found for {ticker} in period {start_date} to {end_date}")
        return []
    
    records = []
    for result in data["results"]:
        date = datetime.fromtimestamp(result['t']/1000).strftime('%Y-%m-%d')
        record = {
            'Date': date,
            'Open': result['o'],
            'High': result['h'],
            'Low': result['l'],
            'Close': result['c'],
            'Volume': result['v'],
            'VWAP': result['vw'] if 'vw' in result else None,
            'Number_of_Transactions': result['n'] if 'n' in result else None
        }
        records.append(record)
    
    return records

def main():
    # Read API key
    api_keys_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'api_keys.txt')
    POLYGON_API_KEY = read_api_key(api_keys_path)
    
    # Calculate date range (2 years from today)
    end_date = datetime.now() - timedelta(days=1)  # Yesterday
    start_date = end_date - timedelta(days=730)  # 365*2 days
    
    # Format dates for API
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')
    
    total_records = 0
    
    for ticker in CRYPTO_PAIRS:
        symbol = ticker.split(':')[1].lower()  # Convert to lowercase for filename
        print(f"\nCollecting data for {ticker} from {start_date_str} to {end_date_str}")
        
        records = get_polygon_data(POLYGON_API_KEY, ticker, start_date_str, end_date_str)
        
        if records:
            # Create DataFrame and save to CSV
            df = pd.DataFrame(records)
            df = df.sort_values('Date')
            
            # Save to individual CSV file with daily_agg in the name
            output_file = f'{symbol}_daily_agg_historical.csv'
            df.to_csv(output_file, index=False)
            
            print(f"Successfully collected {len(records)} days of data for {symbol}")
            print(f"Data saved to {output_file}")
            print("\nLatest data:")
            print(df.tail(1))
            
            total_records += len(records)
        
        # Rate limiting - wait 12 seconds between requests
        if ticker != CRYPTO_PAIRS[-1]:  # Don't wait after the last request
            print("\nWaiting 12 seconds before next request...")
            time.sleep(12)
    
    print(f"\nFinished collecting data for all cryptocurrencies")
    print(f"Total records collected: {total_records}")

if __name__ == "__main__":
    main() 