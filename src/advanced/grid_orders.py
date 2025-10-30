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

def place_grid_orders(symbol, lower_price, upper_price, grids, quantity):
    """Places a simple grid of limit orders between lower and upper price."""
    step = (upper_price - lower_price) / grids
    prices = [round(lower_price + i * step, 2) for i in range(grids + 1)]
    mid = (upper_price + lower_price) / 2

    print(f"\nCreating Grid Orders for {symbol} between {lower_price}-{upper_price} with {grids} grids...\n")
    for p in prices:
        try:
            side = SIDE_BUY if p < mid else SIDE_SELL
            order = client.futures_create_order(
                symbol=symbol,
                side=side,
                type=FUTURE_ORDER_TYPE_LIMIT,
                price=str(p),
                quantity=quantity,
                timeInForce=TIME_IN_FORCE_GTC
            )
            logging.info(f"Grid {side} Order @ {p}")
            print(f"{side} Order placed at {p}")
        except BinanceAPIException as e:
            logging.error(f"Grid Binance API Error: {e}")
            print("Binance API Error:", e.message)
        except Exception as e:
            logging.error(f"Grid Unexpected Error: {e}")
            print("Unexpected Error:", e)
    print("\n✅ Grid setup complete!")

if __name__ == "__main__":
    print("=== Binance Futures Grid Order Bot ===")
    symbol = input("Enter Symbol (e.g., BTCUSDT): ").upper()
    lower_price = float(input("Enter Lower Price: "))
    upper_price = float(input("Enter Upper Price: "))
    grids = int(input("Enter Number of Grids: "))
    quantity = float(input("Enter Quantity per Order: "))

    confirm = input(f"\nConfirm placing grid between {lower_price} and {upper_price}? (y/n): ").lower()
    if confirm == 'y':
        place_grid_orders(symbol, lower_price, upper_price, grids, quantity)
    else:
        print("Grid Setup Cancelled by User.")