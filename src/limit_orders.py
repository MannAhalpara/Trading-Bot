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

def place_limit_order(symbol: str, side: str, quantity: float, price: float, time_in_force: str = "GTC"):
    try:
        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type=FUTURE_ORDER_TYPE_LIMIT,
            timeInForce=time_in_force,
            quantity=quantity,
            price=price,
            timeInforce=time_in_force
        )
        logging.info(f"Limit Order Success | {symbol} | {side} | Qty: {quantity} | Price: {price}")
        print("\n Limit Order Placed Successfully")
        print(f"Symbol: {symbol}")
        print(f"Side: {side}")
        print(f"Quantity: {quantity}")
        print(f"Price: {price}\n")
        print(f"Time in Force: {time_in_force}")
        print(f"Order Details: {order['orderId']}\n")
        return order
    except BinanceAPIException as e:
        logging.error(f"API Error: {e}")
        print("\n Binance API Exception Occurred", e.message)
    except BinanceOrderException as e:
        logging.error(f"Order Error: {e}")
        print("\n Binance Order Exception Occurred", e.message)
    except Exception as e:
        logging.error(f"Unexpected Error: {e}")
        print("\n An error occurred", e)

def cancel_limit_order(symbol: str, order_id: int):
    try:
        result = client.futures_cancel_order(symbol=symbol, orderId=order_id)
        logging.info(f"Order Cancelled | {symbol} | OrderID: {order_id}")
        print(f"\nOrder {order_id} Cancelled Successfully for {symbol}")
        return result
    except BinanceAPIException as e:
        logging.error(f"Cancel Error: {e}")
        print("\nBinance API Exception Occurred:", e.message)
    except Exception as e:
        logging.error(f"Unexpected Error: {e}")
        print("\nUnexpected Error:", e)

if __name__ == "__main__":
    print("=== Binance Futures Limit Order Bot ===")

    symbol = input("Enter Symbol (e.g., BTCUSDT): ").upper()
    side = input("Enter Order Side (BUY/SELL): ").upper()
    quantity = float(input("Enter Order Quantity: "))
    price = float(input("Enter Order Price: "))
    time_in_force = input("Enter Time in Force (GTC/IOC/FOK) [default GTC]: ").upper() or "GTC"

    confirm = input(f"\nConfirm placing {side} limit order for {quantity} {symbol} at price {price}? (y/n): ").lower()
    if confirm == 'y':
        place_limit_order(symbol, side, quantity, price, time_in_force)
    else:
        print("Order Cancelled by User.")