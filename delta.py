from binance.client import Client
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
def get_crypto_ohlc(symbol='BTCUSDT', interval='4h', lookback='2y'):
    """
    Fetch historical OHLC data from Binance
    
    Parameters:
    symbol (str): Trading pair symbol (default: 'BTCUSDT')
    interval (str): Candlestick interval (default: '4h')
    lookback (str): How far back to fetch data (default: '2y')
    
    Returns:
    pandas.DataFrame: OHLC data with columns [timestamp, open, high, low, close, volume]
    """
    # Initialize Binance client (using public API, no keys needed for historical data)
    client = Client()
    
    # Convert interval string to Binance format
    interval_map = {
        '1m': Client.KLINE_INTERVAL_1MINUTE,
        '5m': Client.KLINE_INTERVAL_5MINUTE,
        '15m': Client.KLINE_INTERVAL_15MINUTE,
        '30m': Client.KLINE_INTERVAL_30MINUTE,
        '1h': Client.KLINE_INTERVAL_1HOUR,
        '4h': Client.KLINE_INTERVAL_4HOUR,
        '1d': Client.KLINE_INTERVAL_1DAY,
        '1w': Client.KLINE_INTERVAL_1WEEK,
    }
    
    # Calculate start time based on lookback period
    now = datetime.now()
    if 'y' in lookback:
        start_time = now - timedelta(days=int(lookback.replace('y', '')) * 365)
    elif 'm' in lookback:
        start_time = now - timedelta(days=int(lookback.replace('m', '')) * 30)
    elif 'd' in lookback:
        start_time = now - timedelta(days=int(lookback.replace('d', '')))
    
    # Fetch klines (candlestick data)
    klines = client.get_historical_klines(
        symbol=symbol.upper(),
        interval=interval_map.get(interval, Client.KLINE_INTERVAL_4HOUR),
        start_str=start_time.strftime('%d %b %Y %H:%M:%S'),
    )
    
    # Convert to DataFrame
    df = pd.DataFrame(klines, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'number_of_trades',
        'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
    ])
    
    # Clean up the data
    df = df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    for col in ['open', 'high', 'low', 'close', 'volume']:
        df[col] = df[col].astype(float)
    
    return df

df = get_crypto_ohlc('PENGUUSDT', '4h', '2y')
df['delta%'] = (df['close'].shift(-1) - df['close']) / df['close'] * 100

# Calculate 80th percentile
percentile_95 = df['delta%'].quantile(0.95)
percentile_5 = df['delta%'].quantile(0.05)

# Create histogram of price changes
plt.figure(figsize=(10, 6))
plt.hist(df['delta%'].dropna(), bins=500, edgecolor='black')
plt.axvline(x=percentile_95, color='r', linestyle='--', label=f'95th percentile: {percentile_95:.2f}%')
plt.axvline(x=percentile_5, color='g', linestyle='--', label=f'5th percentile: {percentile_5:.2f}%')
plt.title('Distribution of PENGU Price Changes (%)')
plt.xlabel('Price Change (%)')
plt.ylabel('Frequency')
plt.grid(True, alpha=0.3)
plt.legend()
plt.show()
