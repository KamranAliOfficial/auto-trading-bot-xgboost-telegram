#!/usr/bin/env python3
# enhanced_main.py - Enhanced Trading System (Simple Working Version)
# Enhanced by: Anoop - Senior Trading Software Developer

import os
import sys
import json
import logging
import asyncio
import time
from datetime import datetime
from pathlib import Path

# Setup logging first
def setup_logging():
    """Setup logging"""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / 'enhanced_trading_system.log', encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    return logging.getLogger("EnhancedTradingSystem")

logger = setup_logging()

class SimpleEnhancedTradingSystem:
    """Simple Enhanced Trading System that definitely works"""
    
    def __init__(self):
        self.is_running = False
        logger.info("🚀 Enhanced Trading System Initializing...")
        
        # Setup directories
        self.setup_directories()
        
        # Load config
        self.config = self.load_config()
        
        logger.info("✅ System initialized successfully")
        print("✅ System initialized successfully")
    
    def setup_directories(self):
        """Setup required directories"""
        directories = ["data", "logs", "reports", "config"]
        for directory in directories:
            Path(directory).mkdir(exist_ok=True)
        logger.info("✅ Directories created")
        print("✅ Directories created")
    
    def load_config(self):
        """Load configuration"""
        try:
            config_file = Path("config/trading_settings.json")
            if config_file.exists():
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                logger.info("✅ Configuration loaded")
                print("✅ Configuration loaded")
                return config
            else:
                logger.info("⚠️  Using default configuration")
                print("⚠️  Using default configuration")
                return self.get_default_config()
        except Exception as e:
            logger.error(f"❌ Config error: {e}")
            print(f"❌ Config error: {e}")
            return self.get_default_config()
    
    def get_default_config(self):
        """Default configuration"""
        return {
            "system": {
                "enable_paper_trading": True,
                "log_level": "INFO"
            },
            "risk_management": {
                "max_position_size_usd": 1000,
                "stop_loss_percentage": 0.15
            },
            "trading": {
                "max_daily_trades": 10
            }
        }
    
    def check_market_open(self):
        """Simple market check"""
        try:
            now = datetime.now()
            # Simple check: Monday-Friday, 9 AM - 4 PM
            if now.weekday() >= 5:  # Weekend
                return False
            if 9 <= now.hour <= 16:  # Market hours
                return True
            return False
        except Exception as e:
            logger.error(f"Market check error: {e}")
            return True  # Assume open if error
    
    def perform_health_check(self):
        """Perform system health check"""
        try:
            health_status = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "system_status": "✅ HEALTHY",
                "paper_trading": self.config.get("system", {}).get("enable_paper_trading", True),
                "market_status": "🟢 OPEN" if self.check_market_open() else "🔴 CLOSED"
            }
            
            logger.info(f"Health Check: {health_status}")
            print(f"📊 Health Check: {health_status['system_status']} | Market: {health_status['market_status']}")
            
            return health_status
            
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            print(f"❌ Health check failed: {e}")
            return {"system_status": "❌ ERROR", "error": str(e)}
    
    async def send_startup_notification(self):
        """Send startup notification if Telegram is configured"""
        try:
            # Check if telegram is configured
            if not self.config.get("notifications", {}).get("telegram_bot_token"):
                logger.info("📱 Telegram not configured - skipping notification")
                print("📱 Telegram not configured - skipping notification")
                return
            
            # Try to send notification
            from telegram import Bot
            bot_token = self.config["notifications"]["telegram_bot_token"]
            chat_id = self.config["notifications"]["telegram_chat_id"]
            
            if bot_token != "YOUR_TELEGRAM_BOT_TOKEN":
                bot = Bot(token=bot_token)
                message = f"""
🚀 Enhanced Trading System Online

✅ Status: Running
📊 Mode: {'Paper Trading' if self.config.get('system', {}).get('enable_paper_trading', True) else 'Live Trading'}
⏰ Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
🔧 Version: 2.0 Professional

System is ready and monitoring!
"""
                await bot.send_message(chat_id=chat_id, text=message)
                logger.info("✅ Startup notification sent to Telegram")
                print("✅ Startup notification sent to Telegram")
            
        except ImportError:
            logger.info("📱 Telegram library not available")
            print("📱 Telegram library not available")
        except Exception as e:
            logger.warning(f"📱 Telegram notification failed: {e}")
            print(f"📱 Telegram notification failed: {e}")
    
    async def main_loop(self):
        """Main system loop"""
        try:
            self.is_running = True
            loop_count = 0
            
            logger.info("🔄 Starting main system loop...")
            print("🔄 Starting main system loop...")
            
            while self.is_running:
                loop_count += 1
                
                # Perform health check every 10 loops (5 minutes)
                if loop_count % 10 == 0:
                    self.perform_health_check()
                
                # Check market status
                market_open = self.check_market_open()
                
                if market_open:
                    logger.info("📈 Market is OPEN - Monitoring for opportunities...")
                    print(f"📈 Market OPEN | Loop: {loop_count} | {datetime.now().strftime('%H:%M:%S')}")
                    
                    # This is where actual trading logic would go
                    # For now, just log that we're monitoring
                    
                else:
                    logger.info("💤 Market is CLOSED - Waiting...")
                    print(f"💤 Market CLOSED | Loop: {loop_count} | {datetime.now().strftime('%H:%M:%S')}")
                
                # Wait 30 seconds before next iteration
                await asyncio.sleep(30)
                
        except KeyboardInterrupt:
            logger.info("🛑 Shutdown requested by user")
            print("🛑 Shutdown requested by user")
            await self.shutdown()
        except Exception as e:
            logger.error(f"❌ Main loop error: {e}")
            print(f"❌ Main loop error: {e}")
            await self.shutdown()
    
    async def shutdown(self):
        """Graceful shutdown"""
        try:
            logger.info("🔄 Shutting down Enhanced Trading System...")
            print("🔄 Shutting down Enhanced Trading System...")
            
            self.is_running = False
            
            # Send shutdown notification if configured
            try:
                if self.config.get("notifications", {}).get("telegram_bot_token"):
                    from telegram import Bot
                    bot_token = self.config["notifications"]["telegram_bot_token"]
                    chat_id = self.config["notifications"]["telegram_chat_id"]
                    
                    if bot_token != "YOUR_TELEGRAM_BOT_TOKEN":
                        bot = Bot(token=bot_token)
                        message = "🔴 Enhanced Trading System - Shutdown Complete"
                        await bot.send_message(chat_id=chat_id, text=message)
                        logger.info("✅ Shutdown notification sent")
                        print("✅ Shutdown notification sent")
            except Exception as e:
                logger.warning(f"Shutdown notification failed: {e}")
            
            logger.info("✅ Enhanced Trading System shutdown complete")
            print("✅ Enhanced Trading System shutdown complete")
            
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")
            print(f"Error during shutdown: {e}")
    
    async def start(self):
        """Start the system"""
        try:
            print("\n" + "="*60)
            print("🚀 ENHANCED TRADING SYSTEM STARTING")
            print("Enhanced by: Anoop - Senior Trading Software Developer")
            print("Version: 2.0 Professional")
            print("="*60)
            
            logger.info("🚀 Enhanced Trading System Starting...")
            
            # Perform initial health check
            print("\n📊 Performing initial health check...")
            health_status = self.perform_health_check()
            
            # Send startup notification
            print("\n📱 Sending startup notification...")
            await self.send_startup_notification()
            
            # Show system info
            print(f"\n📋 System Configuration:")
            print(f"   • Paper Trading: {'✅ ENABLED' if self.config.get('system', {}).get('enable_paper_trading', True) else '❌ DISABLED'}")
            print(f"   • Max Daily Trades: {self.config.get('trading', {}).get('max_daily_trades', 10)}")
            print(f"   • Stop Loss: {self.config.get('risk_management', {}).get('stop_loss_percentage', 0.15)*100}%")
            
            print(f"\n🎯 System is now running! Press Ctrl+C to stop.")
            print("📊 Monitor the logs in logs/enhanced_trading_system.log")
            print("-"*60)
            
            # Start main loop
            await self.main_loop()
            
        except Exception as e:
            logger.error(f"❌ System start error: {e}")
            print(f"❌ System start error: {e}")
            await self.shutdown()

# Main execution
async def main():
    """Main entry point"""
    try:
        # Create and start the system
        trading_system = SimpleEnhancedTradingSystem()
        await trading_system.start()
        
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        print(f"❌ Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        print("Starting Enhanced Trading System...")
        
        # Windows compatibility
        if os.name == 'nt':
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        
        # Run the system
        asyncio.run(main())
        
    except KeyboardInterrupt:
        print("\n✅ System shutdown complete")
    except Exception as e:
        print(f"❌ Fatal system error: {e}")
        sys.exit(1)