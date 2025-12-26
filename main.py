import os, time, ccxt
from datetime import datetime
import talib as ta

EXCHANGE = ccxt.binance({
    'apiKey': os.getenv('BINANCE_KEY'),
    'secret': os.getenv('BINANCE_SECRET'),
    'options': {'defaultType': 'spot'},
    'enableRateLimit': True
})

SYMBOL = 'BTC/USDT'
RISK   = 0.02          # 2 %
SL_MULT = 1.8
TP_MULT = 6.0
PARTIAL = 0.4          # 40 % на 2·ATR
TRAIL   = 0.1

def get_atr(candles):
    return ta.atr([c[2] for c in candles], [c[3] for c in candles], [c[4] for c in candles], timeperiod=14)[-1]

side = None; entry = 0; amt = 0; sl = 0; tp1 = 0; tp2 = 0; sold = False

while True:
    try:
        price   = EXCHANGE.fetch_ticker(SYMBOL)['last']
        candles = EXCHANGE.fetch_ohlcv(SYMBOL, '5m', limit=50)
        atr     = get_atr(candles)
        rsi     = ta.rsi([c[4] for c in candles], timeperiod=14)[-1]
        ema200  = ta.ema([c[4] for c in candles], timeperiod=200)[-1]

        if side is None:
            if rsi < 22 and price > ema200:
                balance = float(EXCHANGE.fetch_balance()['USDT']['free'])
                risk_amt = balance * RISK
                amt = risk_amt / price
                amt = EXCHANGE.amount_to_precision(SYMBOL, amt)
                entry = EXCHANGE.create_market_buy_order(SYMBOL, amt)['average']
                sl  = entry - atr * SL_MULT
                tp1 = entry + atr * 2.0
                tp2 = entry + atr * TP_MULT
                EXCHANGE.create_order(SYMBOL, 'OCO', 'sell', amt, tp2, sl, params={'stopPrice': sl})
                sold = False; side = 'long'
                print(datetime.utcnow(), 'BUY', amt, '@', entry)
        else:
            new_sl = price - atr * SL_MULT
            if new_sl > sl:
                sl = new_sl
                for o in EXCHANGE.fetch_open_orders(SYMBOL): EXCHANGE.cancel_order(o['id'], SYMBOL)
                EXCHANGE.create_order(SYMBOL, 'OCO', 'sell', amt, tp2, sl, params={'stopPrice': sl})
            if not sold and price >= tp1:
                part_amt = amt * PARTIAL
                EXCHANGE.create_market_sell_order(SYMBOL, part_amt)
                amt -= part_amt; sold = True
                print(datetime.utcnow(), 'PARTIAL 40 % @', price)
            if price >= tp2:
                EXCHANGE.create_market_sell_order(SYMBOL, amt)
                print(datetime.utcnow(), 'FINAL 60 % @', price); side = None
        time.sleep(5)
    except Exception as e:
        print(e); time.sleep(5)
