import os
import logging
from dotenv import load_dotenv
from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException

# Load credentials
load_dotenv()
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

# Setup client
BASE_URL = "https://testnet.binancefuture.com"
client = Client(API_KEY, API_SECRET, testnet=True)
client.FUTURES_URL = BASE_URL

# Logging setup
logging.basicConfig(
    filename="bot.log",
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s",
)

def place_stop_limit_order(symbol: str, side: str, quantity: float, stop_price: float, limit_price: float):
    """Places a stop-limit order on Binance Futures."""
    try:
        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type=FUTURE_ORDER_TYPE_STOP_MARKET,
            stopPrice=str(stop_price),
            quantity=quantity,
            timeInForce=TIME_IN_FORCE_GTC
        )
        logging.info(f"Stop-Limit Order Placed | {symbol} | {side} | Stop: {stop_price} | Limit: {limit_price} | Qty: {quantity}")
        print(f"\nStop-Limit Order Placed Successfully!")
        print(f"Symbol: {symbol}\nSide: {side}\nStop Price: {stop_price}\nLimit Price: {limit_price}\nQuantity: {quantity}\n")
        print(f"Order ID: {order['orderId']}\n")
        return order
    except BinanceAPIException as e:
        logging.error(f"Binance API Error: {e}")
        print("\nBinance API Exception Occurred:", e.message)
    except Exception as e:
        logging.error(f"Unexpected Error: {e}")
        print("\nUnexpected Error Occurred:", e)

if __name__ == "__main__":
    print("=== Binance Futures Stop-Limit Order Bot ===")

    symbol = input("Enter Symbol (e.g., BTCUSDT): ").upper()
    side = input("Enter Order Side (BUY/SELL): ").upper()
    quantity = float(input("Enter Quantity: "))
    stop_price = float(input("Enter Stop Price: "))
    limit_price = float(input("Enter Limit Price: "))

    confirm = input(f"\nConfirm placing {side} Stop-Limit order for {quantity} {symbol}? (y/n): ").lower()
    if confirm == 'y':
        place_stop_limit_order(symbol, side, quantity, stop_price, limit_price)
    else:
        print("Order Cancelled by User.")