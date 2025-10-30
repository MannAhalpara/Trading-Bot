# 🤖 Binance Futures Trading Bot

A robust, modular Python trading bot designed to execute various advanced order types on the Binance Futures Testnet. This project serves as a foundational framework for developing and testing complex trading strategies safely before deployment in a live environment.

## 🎯 Project Overview and Objectives

The primary objective of this project is to create a set of simple, executable Python scripts that demonstrate proficient interaction with the Binance Futures API (via python-binance). The bot is strictly configured to operate on the Testnet environment to ensure safe development and testing.

Key Objectives:
- **Modular Implementation**: Separate common order types and advanced strategies into distinct, easy-to-manage scripts.
- **Secure Configuration**: Implement secure handling of API credentials using environment variables.
- **Comprehensive Order Types**: Implement core trading logic for basic and advanced strategies, including Market, Limit, Grid, OCO, and TWAP orders.
- **Robust Error Handling**: Include explicit error handling for API and order exceptions.
- **Audit Trail**: Centralize all trade and error activity through a consistent logging mechanism.

## 📁 Folder and File Structure

The repository is structured for clarity, separating core execution scripts from more complex, algorithmic strategies.

```
mann-binance-bot/
├── .gitignore               # Specifies files/folders to exclude from git (e.g., venv, .env)
├── requirements.txt         # List of Python dependencies (python-binance, python-dotenv, etc.)
├── bot.log                  # Log file for all bot actions and errors (auto-generated)
└── src/
    ├── check_order_status.py  # Script to check a specific order status or list recent orders
    ├── limit_orders.py        # Functions to place and cancel Futures Limit orders
    ├── market_orders.py       # Function to place Futures Market orders
    └── advanced/
        ├── grid_orders.py     # Logic for placing a symmetrical price grid of BUY/SELL orders
        ├── oco_order.py       # Simulation of a One-Cancels-the-Other (OCO) strategy
        ├── stop_limit_order.py# Function to place a Stop-Market order
        └── twap_order.py      # Time-Weighted Average Price (TWAP) execution logic
```

## ⚙️ Setup and Installation

### 1. Python and Virtual Environment

It is highly recommended to use a Python virtual environment to manage dependencies.

```bash
# 1. Create a virtual environment
python3 -m venv venv

# 2. Activate the environment (Linux/macOS)
source venv/bin/activate

# 3. Activate the environment (Windows)
.\venv\Scripts\activate
```

### 2. Dependency Installation

Install all required libraries, including python-binance and python-dotenv, using the provided requirements file.

```bash
pip install -r requirements.txt
```

### 3. API Key Configuration (.env file)

For security, API keys are loaded from an environment file, which is excluded from the repository by .gitignore.
Create a file named `.env` in the project root directory and add your Binance Futures Testnet API credentials:

```bash
# .env file content
API_KEY="YOUR_BINANCE_TESTNET_API_KEY"
API_SECRET="YOUR_BINANCE_TESTNET_API_SECRET"
```

## 📜 Order Types Implemented

| File | Order Type | Strategy Description |
|------|------------|---------------------|
| market_orders.py | Market | Executes a trade instantly at the current best available price. |
| limit_orders.py | Limit | Places an order at a specific price, only executing when the price is met. Includes a function for cancellation. |
| stop_limit_order.py | Stop-Market | Places a market order when the designated stop price is reached. |
| oco_order.py | Simulated OCO | Places two separate orders—a Take-Profit (Limit) and a Stop-Loss (Stop-Market)—to simulate a classic OCO bracket. |
| twap_order.py | TWAP | Divides a large order into smaller Market order "chunks" and executes them at regular time intervals (in seconds). |
| grid_orders.py | Grid | Places a symmetric grid of alternating BUY and SELL Limit orders across a defined price range. |

## 🚀 How to Run Each Script

All scripts are executed via the command line and prompt the user for necessary inputs (Symbol, Side, Quantity, Price).

```bash
# Market Order Execution
python3 src/market_orders.py

# Limit Order (and Cancel Order) Execution
python3 src/limit_orders.py

# Stop-Market Order Execution
python3 src/advanced/stop_limit_order.py

# Simulated OCO Order Execution
python3 src/advanced/oco_order.py

# TWAP Order Execution
python3 src/advanced/twap_order.py

# Grid Order Execution
python3 src/advanced/grid_orders.py

# Check Order Status
python3 src/check_order_status.py
```

## 🔒 Logging and Validation

**Logging**: All successful executions, API errors, and order exceptions are logged to a central file named `bot.log`. The format includes timestamp, log level, and message (`%(asctime)s:%(levelname)s:%(message)s`).

**Validation & Error Handling**: The code uses try...except blocks to catch and log specific exceptions from the python-binance library, including `BinanceAPIException` (for API-level issues) and `BinanceOrderException` (for order-related failures), ensuring the bot handles issues gracefully without crashing.

## ⭐ Credits / Author

Author: MannAhalpara
Repository: https://github.com/MannAhalpara/mann-binance-bot
