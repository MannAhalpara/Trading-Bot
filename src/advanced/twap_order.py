import os
import time
import logging
from dotenv import load_dotenv
from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException

load_dotenv()
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

BASE_URL = "https://testnet.binancefuture.com"
client = Client(API_KEY, API_SECRET, testnet=True)
client.FUTURES_URL = BASE_URL

logging.basicConfig(
    filename="bot.log",
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s",
)

def twap_order(symbol, side, total_qty, chunks, interval):
    """Places multiple market orders equally spaced in time (TWAP)."""
    qty_per_order = round(total_qty / chunks, 6)
    print(f"\nPlacing {chunks} TWAP orders of {qty_per_order} each, every {interval} seconds...\n")

    for i in range(chunks):
        try:
            order = client.futures_create_order(
                symbol=symbol,
                side=side,
                type=FUTURE_ORDER_TYPE_MARKET,
                quantity=qty_per_order
            )
            logging.info(f"TWAP {i+1}/{chunks} Success | {symbol} | {side} | Qty: {qty_per_order}")
            print(f"✔️  TWAP Order {i+1}/{chunks} Executed")
        except BinanceAPIException as e:
            logging.error(f"TWAP Binance API Error: {e}")
            print("Binance API Error:", e.message)
        except Exception as e:
            logging.error(f"TWAP Unexpected Error: {e}")
            print("Unexpected Error:", e)
        time.sleep(interval)
    print("\n✅ All TWAP orders completed.")

if __name__ == "__main__":
    print("=== Binance Futures TWAP Bot ===")
    symbol = input("Enter Symbol (e.g., BTCUSDT): ").upper()
    side = input("Enter Side (BUY/SELL): ").upper()
    total_qty = float(input("Enter Total Quantity: "))
    chunks = int(input("Enter Number of Splits: "))
    interval = int(input("Enter Interval in Seconds: "))

    confirm = input(f"\nConfirm TWAP of {total_qty} {symbol} in {chunks} chunks? (y/n): ").lower()
    if confirm == 'y':
        twap_order(symbol, side, total_qty, chunks, interval)
    else:
        print("Order Cancelled by User.")