import os
import logging
from dotenv import load_dotenv
from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException, BinanceOrderException

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

BASE_URL = "https://testnet.binancefuture.com"

client = Client(API_KEY, API_SECRET, testnet=True)
client.FUTURES_URL = BASE_URL

logging.basicConfig(
    filename = "bot.log",
    level = logging.INFO,
    format = "%(asctime)s:%(levelname)s:%(message)s",
)

def place_market_order(symbol: str, side: str, quantity: float):
    try:
        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type=FUTURE_ORDER_TYPE_MARKET,
            quantity=quantity
        )
        logging.info(f"Market Order Success | {symbol} | {side} | Qty: {quantity}")
        print("\n Market Order Placed Successfully")
        print(f"Symbol: {symbol}")
        print(f"Side: {side}")
        print(f"Quantity: {quantity}\n")
        print(f"Order Details: {order['orderId']}\n")
        return order
    
    except BinanceAPIException as e:
        logging.error(f"API Error: {e}")
        print("\n Binance API Exception Occurred", e.message)
    except Exception as e:
        logging.error(f"Unexpected Error: {e}")
        print("\n An error occurred", e)

if __name__ == "__main__":
    print("=== Binance Futures Market Order Bot ===")

    symbol = input("Enter Symbol (e.g., BTCUSDT): ").upper()
    side = input("Enter Order Side (BUY/SELL): ").upper()
    quantity = float(input("Enter Order Quantity: "))

    confirm = input(f"\nConfirm placing {side} market order for {quantity} {symbol}? (y/n): ").lower()
    if confirm == 'y':
        place_market_order(symbol, side, quantity)
    else:
        print("Order Cancelled by User.")