# 🚀 Professional Trading System - Complete Setup Guide

**Enhanced by: Anoop - Senior Trading Software Developer**

## 📋 System Requirements

### Minimum Hardware Requirements
- **CPU**: 4+ cores, 2.5GHz or higher
- **RAM**: 8GB minimum (16GB recommended)
- **Storage**: 50GB free space (SSD recommended)
- **Network**: Stable internet connection (low latency preferred)

### Software Requirements
- **Operating System**: Windows 10/11, macOS 10.15+, or Linux Ubuntu 18.04+
- **Python**: 3.8 or higher
- **Database**: SQLite (included) or PostgreSQL (optional)

## 🔧 Installation Steps

### Step 1: Clone and Setup Repository
```bash
# Clone the repository
git clone https://github.com/your-repo/enhanced-trading-system.git
cd enhanced-trading-system

# Create virtual environment
python -m venv trading_env

# Activate virtual environment
# Windows:
trading_env\Scripts\activate
# macOS/Linux:
source trading_env/bin/activate
```

### Step 2: Install Dependencies
```bash
# Install required packages
pip install -r requirements.txt

# Install additional packages for enhanced features
pip install psycopg2-binary  # For PostgreSQL (optional)
pip install redis           # For caching (optional) 
pip install uvloop          # For better asyncio performance (Linux/macOS)
```

### Step 3: Create Directory Structure
```bash
# Create required directories
mkdir -p data logs reports config/backup models
mkdir -p data/cache data/history data/alerts

# Set permissions (Linux/macOS)
chmod 755 data logs reports
chmod 600 config/trading_settings.json  # Protect config file
```

### Step 4: Configuration Setup

#### A. Create Trading Configuration
```bash
# Copy example configuration
cp config/trading_settings.example.json config/trading_settings.json
```

#### B. Update Configuration File
Edit `config/trading_settings.json`:

```json
{
  "risk_management": {
    "max_position_size_usd": 1000,
    "max_total_exposure_usd": 10000,
    "stop_loss_percentage": 0.15,
    "risk_per_trade_percentage": 0.02
  },
  "notifications": {
    "telegram_bot_token": "YOUR_BOT_TOKEN",
    "telegram_chat_id": "YOUR_CHAT_ID"
  },
  "system": {
    "enable_paper_trading": true
  }
}
```

#### C. Environment Variables
Create `.env` file:
```bash
# Trading API Keys
NEWS_API_KEY=your_news_api_key
ALPHA_VANTAGE_KEY=your_alpha_vantage_key

# Telegram Configuration
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_chat_id

# Database (optional)
DATABASE_URL=postgresql://user:pass@localhost/trading_db

# Security
SECRET_KEY=your_secret_key_here
```

### Step 5: Database Setup (Optional)
```bash
# For PostgreSQL setup
sudo apt install postgresql postgresql-contrib  # Ubuntu
brew install postgresql                         # macOS

# Create database
createdb trading_system

# Run migrations
python scripts/setup_database.py
```

### Step 6: Initial Data Setup
```bash
# Download initial stock symbols
python scripts/update_symbols.py

# Build initial training data
python build_training_data_nasdaq.py

# Train initial ML model
python train_model_full.py
```

## 🔐 Security Configuration

### API Keys and Tokens
1. **Never commit API keys to version control**
2. Use environment variables or encrypted config files
3. Rotate keys regularly
4. Limit API key permissions

### System Security
```bash
# Create dedicated user (Linux)
sudo useradd -m -s /bin/bash trading
sudo usermod -aG trading your_username

# Set file permissions
chmod 600 .env
chmod 700 logs/
chmod 755 scripts/
```

## 📊 Telegram Bot Setup

### Step 1: Create Bot
1. Message `@BotFather` on Telegram
2. Use `/newbot` command
3. Choose bot name and username
4. Save the bot token

### Step 2: Get Chat ID
```bash
# Method 1: Use provided script
python scripts/get_telegram_chat_id.py

# Method 2: Manual method
# 1. Add bot to your chat/group
# 2. Send a message
# 3. Visit: https://api.telegram.org/bot<TOKEN>/getUpdates
# 4. Find "chat":{"id": YOUR_CHAT_ID}
```

### Step 3: Configure Permissions
- Add bot to trading group with admin rights
- Enable notifications in group settings
- Test notifications with test script

## 🧪 Testing the Installation

### Step 1: Run System Tests
```bash
# Run comprehensive test suite
python -m pytest tests/ -v

# Run specific component tests
python tests/test_risk_manager.py
python tests/test_position_manager.py
python tests/test_trader.py
```

### Step 2: Paper Trading Test
```bash
# Start paper trading mode
python enhanced_main.py --paper-trading

# Monitor logs
tail -f logs/trading_system.log
```

### Step 3: Notification Test
```bash
# Test Telegram notifications
python scripts/test_notifications.py
```

## 🚀 Running the System

### Development Mode
```bash
# Run with debug logging
python enhanced_main.py --debug

# Run with specific config
python enhanced_main.py --config config/dev_settings.json
```

### Production Mode
```bash
# Run as service (Linux)
sudo systemctl start trading-system

# Run with process manager
pm2 start enhanced_main.py --name trading-system

# Run with screen (simple approach)
screen -S trading python enhanced_main.py
```

### Docker Deployment (Recommended)
```bash
# Build image
docker build -t trading-system .

# Run container
docker run -d \
  --name trading-system \
  --restart unless-stopped \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/config:/app/config \
  --env-file .env \
  trading-system
```

## 📈 Monitoring and Maintenance

### System Health Monitoring
```bash
# Check system status
python scripts/health_check.py

# View performance metrics
python scripts/performance_dashboard.py

# Check position status
python scripts/position_status.py
```

### Log Management
```bash
# View real-time logs
tail -f logs/trading_system.log

# Search logs
grep "ERROR" logs/trading_system.log
grep "TRADE_EXECUTED" logs/trading_system.log

# Rotate logs
python scripts/rotate_logs.py
```

### Backup and Recovery
```bash
# Create system backup
python scripts/backup_system.py

# Restore from backup
python scripts/restore_backup.py --backup-file backup_20241201.tar.gz
```

## ⚙️ Performance Optimization

### System Optimization
```bash
# Optimize Python performance
export PYTHONOPTIMIZE=1

# Use faster JSON library (optional)
pip install orjson

# Enable memory optimization
export PYTHONMALLOC=malloc
```

### Network Optimization
- Use a VPS close to financial data centers
- Configure DNS for faster lookups
- Use connection pooling for API calls

### Database Optimization (if using PostgreSQL)
```sql
-- Create indexes for better performance
CREATE INDEX idx_positions_symbol ON positions(symbol);
CREATE INDEX idx_trades_timestamp ON trades(timestamp);
CREATE INDEX idx_prices_symbol_timestamp ON prices(symbol, timestamp);
```

## 🐛 Troubleshooting

### Common Issues

#### Issue: "Module not found" errors
```bash
# Solution: Ensure virtual environment is activated
source trading_env/bin/activate
pip install -r requirements.txt
```

#### Issue: Telegram notifications not working
```bash
# Check bot token and chat ID
python scripts/test_telegram.py

# Verify bot permissions
# Ensure bot is admin in the group
```

#### Issue: Market data not updating
```bash
# Check API limits
python scripts/check_api_limits.py

# Test data sources
python scripts/test_data_sources.py
```

#### Issue: Trades not executing
```bash
# Check paper trading mode
grep "paper_trading" config/trading_settings.json

# Verify risk limits
python scripts/check_risk_limits.py
```

### Debug Mode
```bash
# Enable detailed logging
export LOG_LEVEL=DEBUG
python enhanced_main.py

# Enable profiling
python -m cProfile enhanced_main.py > performance.prof
```

## 📞 Support and Updates

### Getting Help
1. Check this documentation first
2. Review log files for error details
3. Run diagnostic scripts
4. Check GitHub issues
5. Contact: anoop@tradingsystem.com

### System Updates
```bash
# Check for updates
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Run migration scripts
python scripts/migrate_data.py

# Restart system
python scripts/restart_system.py
```

### Performance Monitoring
- **Daily**: Check position reports
- **Weekly**: Review performance metrics
- **Monthly**: Analyze trading statistics
- **Quarterly**: Rebalance risk parameters

## 🎯 Next Steps

1. **Complete Installation**: Follow all steps above
2. **Paper Trading**: Run in paper mode for 1-2 weeks
3. **Performance Review**: Analyze results and adjust settings
4. **Live Trading**: Switch to live mode with small position sizes
5. **Scale Up**: Gradually increase position sizes based on performance

## ⚠️ Important Disclaimers

- **PAPER TRADING FIRST**: Always test thoroughly in paper trading mode
- **START SMALL**: Begin with minimal position sizes in live trading
- **RISK MANAGEMENT**: Never risk more than you can afford to lose
- **MONITORING**: Always monitor the system actively
- **COMPLIANCE**: Ensure compliance with local financial regulations

---

**System Enhanced by: Anoop - Senior Trading Software Developer**  
**Version**: 2.0 Professional  
**Last Updated**: December 2024  
**Contact**: anoop@tradingsystem.com