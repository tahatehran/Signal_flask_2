import pandas as pd
import ta

def get_buy_sell_signals(data):
    df = pd.DataFrame([data])
    if len(df) < 14:  # RSI و SMA نیاز به حداقل 14 داده دارند
        return {
            'buy_signal': False,
            'sell_signal': False,
            'rsi': None,
            'sma': None
        }
        
    df['rsi'] = ta.momentum.rsi(df['price'], window=14)
    df['sma'] = ta.trend.sma_indicator(df['price'], window=14)
    
    df['buy_signal'] = (df['rsi'] < 30) & (df['price'] > df['sma'])
    df['sell_signal'] = (df['rsi'] > 70) & (df['price'] < df['sma'])
    
    return df.to_dict(orient='records')[0]
  
