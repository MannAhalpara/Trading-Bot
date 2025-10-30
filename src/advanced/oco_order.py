import os
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

def place_oco_futures(symbol, side, quantity, take_profit, stop_loss):
    """Simulates an OCO order on Binance Futures."""
    try:
        # 1️⃣ Take-Profit Limit
        tp_order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type=FUTURE_ORDER_TYPE_LIMIT,
            price=str(take_profit),
            quantity=quantity,
            timeInForce=TIME_IN_FORCE_GTC
        )

        # 2️⃣ Stop-Loss Market
        sl_order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type=FUTURE_ORDER_TYPE_STOP_MARKET,
            stopPrice=str(stop_loss),
            quantity=quantity
        )

        logging.info(f"OCO Simulated | {symbol} | {side} | TP: {take_profit} | SL: {stop_loss}")
        print(f"\nOCO Simulated Orders Placed Successfully!")
        print(f"Take Profit @ {take_profit}")
        print(f"Stop Loss @ {stop_loss}\n")
        print(f"TP Order ID: {tp_order['orderId']} | SL Order ID: {sl_order['orderId']}")
        return tp_order, sl_order
    except BinanceAPIException as e:
        logging.error(f"Binance API Error: {e}")
        print("\nBinance API Exception Occurred:", e.message)
    except Exception as e:
        logging.error(f"Unexpected Error: {e}")
        print("\nUnexpected Error Occurred:", e)

if __name__ == "__main__":
    print("=== Binance Futures Simulated OCO Bot ===")
    symbol = input("Enter Symbol (e.g., BTCUSDT): ").upper()
    side = input("Enter Side (SELL/BUY): ").upper()
    quantity = float(input("Enter Quantity: "))
    take_profit = float(input("Enter Take Profit Price: "))
    stop_loss = float(input("Enter Stop Loss Price: "))

    confirm = input(f"\nConfirm simulated OCO ({side}) for {quantity} {symbol}? (y/n): ").lower()
    if confirm == 'y':
        place_oco_futures(symbol, side, quantity, take_profit, stop_loss)
    else:
        print("Order Cancelled by User.")