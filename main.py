from delta import get_crypto_ohlc

### config #### 
symbol = 'PENGUUSDT'
interval = '4h'
lookback = '2y'

def main(symbol, interval, lookback):
    df = get_crypto_ohlc(symbol, interval, lookback)
    df['delta%'] = (df['close'].shift(-1) - df['close']) / df['close'] * 100
    percentile_95 = df['delta%'].quantile(0.95)
    percentile_5 = df['delta%'].quantile(0.05)
    print(f"95th percentile: {percentile_95:.2f}%")
    print(f"5th percentile: {percentile_5:.2f}%")

main(symbol, interval, lookback)