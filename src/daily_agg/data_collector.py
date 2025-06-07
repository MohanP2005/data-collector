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

def update_crypto_data(api_key, ticker, yesterday_str):
    symbol = ticker.split(':')[1].lower()
    csv_file = f'{symbol}_daily_agg_historical.csv'
    
    if os.path.exists(csv_file):
        print(f"\nReading existing data for {symbol} from {csv_file}")
        df = pd.read_csv(csv_file)
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Remove any future dates
        yesterday = datetime.strptime(yesterday_str, '%Y-%m-%d')
        df = df[df['Date'] <= yesterday]
        
        if len(df) > 0:
            latest_date = df['Date'].max()
            print(f"Latest date in CSV: {latest_date.strftime('%Y-%m-%d')}")
            
            # Calculate the next date we need data for
            start_date = (latest_date + timedelta(days=1)).strftime('%Y-%m-%d')
            
            if start_date <= yesterday_str:
                print(f"Fetching data for period: {start_date} to {yesterday_str}")
                new_records = get_polygon_data(api_key, ticker, start_date, yesterday_str)
                
                if new_records:
                    new_df = pd.DataFrame(new_records)
                    new_df['Date'] = pd.to_datetime(new_df['Date'])
                    
                    # Remove any duplicates
                    new_df = new_df[~new_df['Date'].isin(df['Date'])]
                    
                    if len(new_df) > 0:
                        # Append new data and sort
                        df = pd.concat([df, new_df], ignore_index=True)
                        df = df.sort_values('Date')
                        
                        # Save updated data
                        df.to_csv(csv_file, index=False)
                        print(f"Added {len(new_df)} new records")
                        print("\nLatest data added:")
                        print(new_df.tail(1))
                        return len(new_df)
                    else:
                        print("No new unique data to add")
                else:
                    print("No new data found for the period")
            else:
                print("Data is already up to date")
        else:
            print("No valid data found in CSV")
    else:
        print(f"CSV file not found. Please run historical_data_collector.py first to create {csv_file}")
    
    return 0

def main():
    # Read API key
    api_keys_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'api_keys.txt')
    POLYGON_API_KEY = read_api_key(api_keys_path)
    
    # Get yesterday's date (since today's data might not be complete)
    yesterday = datetime.now() - timedelta(days=1)
    yesterday_str = yesterday.strftime('%Y-%m-%d')
    
    total_new_records = 0
    
    for ticker in CRYPTO_PAIRS:
        new_records = update_crypto_data(POLYGON_API_KEY, ticker, yesterday_str)
        total_new_records += new_records
        
        # Rate limiting - wait 12 seconds between requests
        if ticker != CRYPTO_PAIRS[-1] and new_records > 0:  # Only wait if we made a request
            print("\nWaiting 12 seconds before next request...")
            time.sleep(12)
    
    print(f"\nFinished updating all cryptocurrencies")
    print(f"Total new records added: {total_new_records}")

if __name__ == "__main__":
    main() 