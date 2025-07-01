Auto-Trading Bot with XGBoost and Telegram
A Python-based automated trading bot that leverages the XGBoost machine learning algorithm for trading signal generation and integrates with Telegram for real-time trade notifications and control. This bot is designed to execute trades on supported exchanges, analyze market data, and provide users with actionable insights through a Telegram interface.
Features

Machine Learning Predictions: Utilizes XGBoost to predict market movements based on historical and real-time data.
Telegram Integration: Receive trade signals, manage trades, and monitor performance via Telegram commands.
Real-Time Trading: Executes buy/sell orders using exchange APIs with real-time market data via WebSocket.
Trade History and Analytics: Stores trade data in a database for performance tracking and analysis.
Customizable Strategies: Configure trading parameters and strategies through a configuration file.
Supported Exchanges: Compatible with major exchanges like Binance and BitMEX (testnet available for safe testing).
Risk Management: Implements stop-loss and take-profit levels for controlled trading.

Prerequisites

Python 3.8+
Telegram account and BotFather-created bot token
API keys for supported exchanges (e.g., Binance, BitMEX)
SQLite or another database for trade logging (optional)
Required Python libraries (listed in requirements.txt)

Installation

Clone the Repository
git clone https://github.com/KamranAliOfficial/auto-trading-bot-xgboost-telegram.git
cd auto-trading-bot-xgboost-telegram


Set Up a Virtual Environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install Dependencies
pip install -r requirements.txt


Configure the Bot

Copy config.example.yaml to config.yaml:
cp config.example.yaml config.yaml


Edit config.yaml to include:

Telegram bot token and chat ID
Exchange API key and secret
Trading parameters (e.g., lot size, stop-loss, take-profit)
Database path (if applicable)




Set Up Telegram Bot

Create a bot using BotFather on Telegram to obtain a bot token.
Add the bot to a Telegram group or chat and note the chat ID.



Usage

Run the Bot
python main.py


Telegram Commands

/start: Initialize the bot and check status.
/trade: View current open trades.
/stats: Display trading performance (win/loss, profit).
/buy [symbol] [amount]: Place a manual buy order.
/sell [symbol] [amount]: Place a manual sell order.
/stop: Stop the bot.


Backtesting

To test strategies on historical data:
python backtest.py --symbol BTCUSDT --start_date 2024-01-01 --end_date 2025-01-01




Training the XGBoost Model

Train the model with historical data:
python train_model.py --data data/historical_data.csv --modelname my_model





Configuration
Example config.yaml:
telegram:
  token: "YOUR_BOT_TOKEN"
  chat_id: "YOUR_CHAT_ID"
exchange:
  name: "binance"
  api_key: "YOUR_API_KEY"
  api_secret: "YOUR_API_SECRET"
trading:
  symbol: "BTCUSDT"
  lot_size: 0.01
  stop_loss: 0.02
  take_profit: 0.05
database:
  path: "trades.db"
xgboost:
  max_depth: 8
  learning_rate: 0.01
  num_class: 3

Notes

Risk Warning: Trading involves significant risk. Test the bot in a demo account or dry-run mode before using real funds.
Exchange Support: Ensure your exchange supports API trading. Testnet APIs are recommended for initial testing.
Model Training: Regularly retrain the XGBoost model with fresh data to maintain prediction accuracy.
Dependencies: Ensure all required libraries (e.g., xgboost, python-telegram-bot, ccxt) are installed.

Contributing
Contributions are welcome! Please:

Fork the repository.
Create a feature branch (git checkout -b feature/YourFeature).
Commit changes (git commit -m 'Add YourFeature').
Push to the branch (git push origin feature/YourFeature).
Open a pull request.

License
This project is licensed under the MIT License. See the LICENSE file for details.
Disclaimer
This software is for educational purposes only. Use at your own risk. The authors are not responsible for any financial losses incurred.
