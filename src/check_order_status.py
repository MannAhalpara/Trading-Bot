import os
import logging
from dotenv import load_dotenv
from binance.client import Client
from binance.exceptions import BinanceAPIException

# === Load environment variables ===
load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

# === Binance Futures Testnet Base URL ===
BASE_URL = "https://testnet.binancefuture.com"

# === Initialize Binance Client ===
client = Client(API_KEY, API_SECRET, testnet=True)
client.FUTURES_URL = BASE_URL

# === Configure Logging ===
logging.basicConfig(
    filename="bot.log",
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s",
)

# === Function to Check Order Status ===
def check_order_status(symbol: str, order_id: int):
    """
    Fetch and display details for a specific futures order.
    """
    try:
        order = client.futures_get_order(symbol=symbol, orderId=order_id)

        print("\n=== Binance Futures Order Status ===")
        print(f"Symbol: {order['symbol']}")
        print(f"Order ID: {order['orderId']}")
        print(f"Side: {order['side']}")
        print(f"Type: {order['type']}")
        print(f"Status: {order['status']}")
        print(f"Executed Quantity: {order['executedQty']}")
        print(f"Average Price: {order['avgPrice']}")
        print(f"Reduce Only: {order['reduceOnly']}")
        print(f"Update Time: {order['updateTime']}")
        print("===============================")

        logging.info(f"Checked Order Status | {symbol} | {order_id} | Status: {order['status']}")
        return order

    except BinanceAPIException as e:
        logging.error(f"API Error while checking order: {e}")
        print("\n❌ Binance API Exception Occurred:", e.message)
    except Exception as e:
        logging.error(f"Unexpected Error while checking order: {e}")
        print("\n⚠️ Unexpected Error:", e)

# === Function to View Recent Orders ===
def list_recent_orders(symbol: str, limit: int = 5):
    """
    Fetch and display the most recent futures orders for a given symbol.
    """
    try:
        orders = client.futures_get_all_orders(symbol=symbol, limit=limit)
        print(f"\n=== Last {limit} Orders for {symbol} ===")
        for order in orders[-limit:]:
            print(f"OrderID: {order['orderId']} | Side: {order['side']} | "
                  f"Status: {order['status']} | Qty: {order['origQty']} | Price: {order['avgPrice']}")
        print("===============================")

        logging.info(f"Fetched last {limit} orders for {symbol}")
        return orders

    except BinanceAPIException as e:
        logging.error(f"API Error while listing orders: {e}")
        print("\n❌ Binance API Exception Occurred:", e.message)
    except Exception as e:
        logging.error(f"Unexpected Error while listing orders: {e}")
        print("\n⚠️ Unexpected Error:", e)

# === Main Execution ===
if __name__ == "__main__":
    print("=== Binance Futures Order Status Checker ===")

    symbol = input("Enter Symbol (e.g., BTCUSDT): ").upper()
    choice = input("\nDo you want to:\n1️⃣ Check a specific order\n2️⃣ View recent orders\nChoose (1/2): ")

    if choice == '1':
        order_id = int(input("Enter Order ID: "))
        check_order_status(symbol, order_id)
    elif choice == '2':
        limit = int(input("How many recent orders to display? (default 5): ") or 5)
        list_recent_orders(symbol, limit)
    else:
        print("❌ Invalid choice. Please select 1 or 2.")
