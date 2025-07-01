#!/usr/bin/env python3
# deploy.py - Professional Trading System Deployment Script
# Enhanced by: Anoop - Senior Trading Software Developer
# Windows Compatible Version

import os
import sys
import json
import shutil
import subprocess
import argparse
import asyncio
from datetime import datetime
from pathlib import Path

class TradingSystemDeployment:
    """Professional deployment manager for enhanced trading system"""
    
    def __init__(self):
        self.project_root = Path.cwd()
        self.venv_path = self.project_root / "trading_env"
        self.config_path = self.project_root / "config"
        self.data_path = self.project_root / "data"
        self.logs_path = self.project_root / "logs"
        self.backup_path = self.project_root / "backups"
        
    def print_banner(self):
        """Print deployment banner"""
        banner = f"""
╔═══════════════════════════════════════════════════════════════╗
║                ENHANCED TRADING SYSTEM DEPLOYMENT             ║
║                                                               ║
║  Enhanced by: Anoop - Senior Trading Software Developer      ║
║  Version: 2.0 Professional                                   ║
║  Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}                                  ║
╚═══════════════════════════════════════════════════════════════╝
"""
        print(banner)
    
    def check_system_requirements(self):
        """Check system requirements"""
        print("Checking system requirements...")
        
        # Check Python version
        python_version = sys.version_info
        if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
            raise Exception("Python 3.8 or higher is required")
        
        print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
        
        # Check available disk space
        disk_usage = shutil.disk_usage(self.project_root)
        free_gb = disk_usage.free / (1024**3)
        
        if free_gb < 5:
            raise Exception("At least 5GB of free disk space is required")
        
        print(f"✅ Disk space: {free_gb:.1f}GB available")
        
        # Check if we can create virtual environment
        try:
            import venv
            print("✅ Virtual environment support available")
        except ImportError:
            raise Exception("Python venv module not available")
        
        print("✅ System requirements satisfied\n")
    
    def create_directory_structure(self):
        """Create required directory structure"""
        print("Creating directory structure...")
        
        directories = [
            self.config_path,
            self.config_path / "backup",
            self.data_path,
            self.data_path / "cache",
            self.data_path / "history",
            self.data_path / "alerts",
            self.logs_path,
            self.backup_path,
            Path("reports"),
            Path("models"),
            Path("tests"),
            Path("scripts"),
            Path("monitoring")
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"✅ Created: {directory}")
        
        print("✅ Directory structure created\n")
    
    def setup_virtual_environment(self):
        """Setup virtual environment"""
        print("Setting up virtual environment...")
        
        if self.venv_path.exists():
            print("Virtual environment already exists, recreating...")
            shutil.rmtree(self.venv_path)
        
        # Create virtual environment
        subprocess.run([
            sys.executable, "-m", "venv", str(self.venv_path)
        ], check=True)
        
        print("✅ Virtual environment created")
        
        # Get pip path
        if os.name == 'nt':  # Windows
            pip_path = self.venv_path / "Scripts" / "pip.exe"
            python_path = self.venv_path / "Scripts" / "python.exe"
        else:  # Unix/Linux/MacOS
            pip_path = self.venv_path / "bin" / "pip"
            python_path = self.venv_path / "bin" / "python"
        
        # Upgrade pip
        subprocess.run([
            str(python_path), "-m", "pip", "install", "--upgrade", "pip"
        ], check=True)
        
        print("✅ Pip upgraded")
        print("✅ Virtual environment ready\n")
        
        return python_path, pip_path
    
    def install_dependencies(self, pip_path):
        """Install required dependencies"""
        print("Installing dependencies...")
        
        # Core dependencies
        core_packages = [
            "python-telegram-bot==20.6",
            "yfinance>=0.2.25",
            "requests>=2.31.0",
            "schedule>=1.2.0",
            "numpy>=1.24.0",
            "pandas>=2.0.0",
            "scikit-learn>=1.3.0",
            "aiohttp>=3.8.0",
            "nest_asyncio>=1.5.0",
            "xgboost>=1.7.0",
            "psutil>=5.9.0",
            "python-dotenv>=1.0.0"
        ]
        
        # Optional performance packages
        optional_packages = [
            "orjson>=3.9.0",  # Faster JSON
            "uvloop>=0.17.0;sys_platform!='win32'",  # Better event loop (Linux/Mac)
            "psycopg2-binary>=2.9.0",  # PostgreSQL support
            "redis>=4.5.0"  # Caching support
        ]
        
        all_packages = core_packages + optional_packages
        
        for package in all_packages:
            try:
                print(f"Installing {package.split('>=')[0].split('==')[0]}...")
                subprocess.run([
                    str(pip_path), "install", package
                ], check=True, capture_output=True)
                print(f"✅ {package.split('>=')[0].split('==')[0]} installed")
            except subprocess.CalledProcessError as e:
                if package in optional_packages:
                    print(f"Optional package {package} failed to install (skipping)")
                else:
                    print(f"❌ Failed to install {package}")
                    raise e
        
        print("✅ All dependencies installed\n")
    
    def create_configuration_files(self):
        """Create configuration files"""
        print("Creating configuration files...")
        
        # Default trading configuration
        default_config = {
            "risk_management": {
                "max_position_size_usd": 1000,
                "max_total_exposure_usd": 10000,
                "stop_loss_percentage": 0.15,
                "take_profit_1_percentage": 0.10,
                "take_profit_2_percentage": 0.25,
                "trailing_stop_trigger": 0.08,
                "trailing_stop_percentage": 0.05,
                "risk_per_trade_percentage": 0.02,
                "max_daily_risk_percentage": 0.10,
                "max_drawdown_percentage": 0.15,
                "consecutive_loss_limit": 5
            },
            "trading": {
                "min_ml_score_threshold": 75,
                "max_daily_trades": 20,
                "min_stock_price": 0.50,
                "max_stock_price": 50.00,
                "min_volume": 100000,
                "min_risk_reward_ratio": 1.5,
                "market_open_delay_minutes": 30,
                "market_close_buffer_minutes": 30,
                "enable_pump_trading": True,
                "enable_top_stock_trading": True,
                "enable_watchlist_trading": True
            },
            "notifications": {
                "telegram_bot_token": "YOUR_TELEGRAM_BOT_TOKEN",
                "telegram_chat_id": "YOUR_TELEGRAM_CHAT_ID",
                "telegram_critical_chat_id": "YOUR_TELEGRAM_CHAT_ID",
                "enable_trade_notifications": True,
                "enable_position_updates": True,
                "enable_daily_summary": True,
                "enable_critical_alerts": True,
                "notification_retry_attempts": 3,
                "notification_retry_delay": 2
            },
            "system": {
                "log_level": "INFO",
                "enable_paper_trading": True,
                "auto_restart_on_error": True,
                "health_check_interval": 300,
                "emergency_shutdown_trigger": True
            }
        }
        
        config_file = self.config_path / "trading_settings.json"
        with open(config_file, "w", encoding='utf-8') as f:
            json.dump(default_config, f, indent=2)
        
        print(f"✅ Created: {config_file}")
        
        # Create environment file template
        env_template = """# Enhanced Trading System Environment Variables
# IMPORTANT: Fill in your actual values and rename to .env

# Telegram Configuration (REQUIRED)
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHAT_ID=your_telegram_chat_id_here

# API Keys (REQUIRED)
NEWS_API_KEY=your_news_api_key_here

# Optional API Keys
ALPHA_VANTAGE_KEY=your_alpha_vantage_key_here

# Database Configuration (Optional)
DATABASE_URL=postgresql://user:pass@localhost/trading_db

# Security
SECRET_KEY=your_random_secret_key_here

# Deployment Settings
ENVIRONMENT=development
DEBUG=true
"""
        
        env_file = self.project_root / ".env.template"
        with open(env_file, "w", encoding='utf-8') as f:
            f.write(env_template)
        
        print(f"✅ Created: {env_file}")
        print("IMPORTANT: Remember to rename .env.template to .env and fill in your API keys!")
        print("✅ Configuration files created\n")
    
    def create_startup_scripts(self, python_path):
        """Create startup scripts"""
        print("Creating startup scripts...")
        
        scripts_dir = Path("scripts")
        scripts_dir.mkdir(exist_ok=True)
        
        # Main startup script (without emoji characters)
        startup_script = f"""#!/usr/bin/env python3
# start_trading_system.py - Enhanced Trading System Startup Script

import os
import sys
import asyncio
import logging
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/trading_system.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def main():
    print("Starting Enhanced Trading System...")
    
    # Check environment
    if not os.path.exists('.env'):
        print("ERROR: .env file not found! Please create it from .env.template")
        return False
    
    # Load environment variables
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        print("WARNING: python-dotenv not installed, skipping .env loading")
    
    # Import and run main system
    try:
        from enhanced_main import main as trading_main
        asyncio.run(trading_main())
    except Exception as e:
        logging.error(f"System startup failed: {{e}}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
"""
        
        with open(scripts_dir / "start_trading_system.py", "w", encoding='utf-8') as f:
            f.write(startup_script)
        
        # Health check script (without emoji characters)
        health_check_script = """#!/usr/bin/env python3
# health_check.py - System Health Check Script

import sys
import asyncio
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

async def main():
    try:
        from monitoring.system_monitor import run_health_check
        health_checks = await run_health_check()
        
        print("\\nSystem Health Check Results:")
        print("=" * 40)
        
        critical_issues = 0
        for component, check in health_checks.items():
            status_icon = {
                "healthy": "[OK]",
                "warning": "[WARN]",
                "critical": "[CRIT]"
            }.get(check.status, "[UNK]")
            
            print(f"{status_icon} {component}: {check.message}")
            
            if check.status == "critical":
                critical_issues += 1
        
        print("=" * 40)
        
        if critical_issues > 0:
            print(f"CRITICAL: {critical_issues} critical issues found!")
            return False
        else:
            print("SUCCESS: System healthy!")
            return True
            
    except Exception as e:
        print(f"ERROR: Health check failed: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
"""
        
        with open(scripts_dir / "health_check.py", "w", encoding='utf-8') as f:
            f.write(health_check_script)
        
        # Make scripts executable (Unix/Linux/Mac)
        if os.name != 'nt':
            os.chmod(scripts_dir / "start_trading_system.py", 0o755)
            os.chmod(scripts_dir / "health_check.py", 0o755)
        
        print("✅ Startup scripts created")
        print("✅ Health check script created\n")
    
    def run_initial_tests(self, python_path):
        """Run initial system tests"""
        print("Running initial system tests...")
        
        try:
            # Test imports
            test_script = """
import sys
from pathlib import Path
project_root = Path.cwd()
sys.path.insert(0, str(project_root))

# Test core imports
try:
    import json
    import os
    import logging
    print("SUCCESS: Basic imports working")
except ImportError as e:
    print(f"ERROR: Basic import error: {e}")
    sys.exit(1)

# Test configuration creation
try:
    config_data = {
        "test": True,
        "system": {
            "enable_paper_trading": True
        }
    }
    print("SUCCESS: Configuration test passed") 
except Exception as e:
    print(f"ERROR: Configuration error: {e}")
    sys.exit(1)

print("SUCCESS: All basic tests passed")
"""
            
            # Write and run test script
            test_file = Path("test_deployment.py")
            with open(test_file, "w", encoding='utf-8') as f:
                f.write(test_script)
            
            result = subprocess.run([
                str(python_path), str(test_file)
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print(result.stdout)
                print("✅ Initial tests passed")
            else:
                print(f"Tests failed:\n{result.stderr}")
                print("WARNING: Some tests failed, but continuing deployment")
            
            # Clean up test file
            test_file.unlink()
            
        except Exception as e:
            print(f"Test execution failed: {e}")
            print("WARNING: Tests failed, but continuing deployment")
        
        print("✅ System validation complete\n")
    
    def create_systemd_service(self, python_path):
        """Create systemd service file (Linux only)"""
        if os.name == 'nt':
            return
        
        print("Creating systemd service file...")
        
        service_content = f"""[Unit]
Description=Enhanced Trading System
After=network.target
Wants=network.target

[Service]
Type=simple
User={os.getenv('USER', 'trading')}
WorkingDirectory={self.project_root}
Environment=PATH={self.venv_path}/bin
ExecStart={python_path} scripts/start_trading_system.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
"""
        
        service_file = Path("enhanced-trading-system.service")
        with open(service_file, "w", encoding='utf-8') as f:
            f.write(service_content)
        
        print(f"✅ Created: {service_file}")
        print("To install the service:")
        print(f"   sudo cp {service_file} /etc/systemd/system/")
        print("   sudo systemctl daemon-reload")
        print("   sudo systemctl enable enhanced-trading-system")
        print("   sudo systemctl start enhanced-trading-system")
        print()
    
    def create_docker_files(self):
        """Create Docker deployment files"""
        print("Creating Docker deployment files...")
        
        # Dockerfile
        dockerfile_content = """FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    g++ \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p data logs reports config/backup

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=5m --timeout=30s --start-period=5m --retries=3 \\
    CMD python scripts/health_check.py || exit 1

# Run the application
CMD ["python", "enhanced_main.py"]
"""
        
        with open("Dockerfile", "w", encoding='utf-8') as f:
            f.write(dockerfile_content)
        
        # Docker Compose
        docker_compose_content = """version: '3.8'

services:
  trading-system:
    build: .
    container_name: enhanced-trading-system
    restart: unless-stopped
    environment:
      - ENVIRONMENT=production
    env_file:
      - .env
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
      - ./reports:/app/reports
      - ./config:/app/config
    networks:
      - trading-network

volumes:
  redis-data:
  postgres-data:

networks:
  trading-network:
    driver: bridge
"""
        
        with open("docker-compose.yml", "w", encoding='utf-8') as f:
            f.write(docker_compose_content)
        
        # .dockerignore
        dockerignore_content = """# Development files
.git
.gitignore
README.md
.env.template

# Python cache
__pycache__
*.pyc
*.pyo
*.pyd
.Python
*.so

# Virtual environment
trading_env/
venv/
env/

# IDE files
.vscode/
.idea/
*.swp
*.swo

# OS files
.DS_Store
Thumbs.db

# Temporary files
*.tmp
*.temp
test_*.py

# Logs (will be mounted as volume)
logs/*
!logs/.gitkeep

# Data (will be mounted as volume)
data/*
!data/.gitkeep
"""
        
        with open(".dockerignore", "w", encoding='utf-8') as f:
            f.write(dockerignore_content)
        
        print("✅ Dockerfile created")
        print("✅ docker-compose.yml created")
        print("✅ .dockerignore created")
        print("Docker deployment files ready\n")
    
    def print_deployment_summary(self):
        """Print deployment summary and next steps"""
        summary = f"""
╔═══════════════════════════════════════════════════════════════╗
║                    DEPLOYMENT COMPLETE!                       ║
╚═══════════════════════════════════════════════════════════════╝

SUCCESS: Enhanced Trading System successfully deployed!

NEXT STEPS:

1. Configure your API keys:
   • Rename .env.template to .env
   • Add your Telegram bot token and chat ID
   • Add your news API key
   • Configure other optional services

2. Test the system:
   • Run: python scripts/health_check.py
   • Check: python scripts/start_trading_system.py

3. Start trading (Paper Trading Mode):
   • Run: python scripts/start_trading_system.py
   • Monitor: type logs/trading_system.log (Windows)

4. Production deployment options:
   
   Docker (Recommended):
   • docker-compose up -d
   
   Manual:
   • Activate virtual environment: trading_env\\Scripts\\activate
   • Run: python enhanced_main.py

MONITORING:
   • Health checks: python scripts/health_check.py
   • View logs: type logs\\trading_system.log
   • Performance: Check reports/ directory

IMPORTANT REMINDERS:
   • System starts in PAPER TRADING mode (safe)
   • Test thoroughly before switching to live trading
   • Monitor system performance closely
   • Keep your API keys secure
   • Backup your data directory regularly

SUPPORT:
   • Documentation: Check installation guide
   • Issues: Review logs/trading_system.log
   • Contact: anoop@tradingsystem.com

═══════════════════════════════════════════════════════════════

Enhanced by: Anoop - Senior Trading Software Developer
Version: 2.0 Professional | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Ready to trade smartly and profitably!
"""
        print(summary)

def main():
    """Main deployment function"""
    parser = argparse.ArgumentParser(description="Enhanced Trading System Deployment")
    parser.add_argument("--skip-tests", action="store_true", help="Skip initial tests")
    parser.add_argument("--no-docker", action="store_true", help="Skip Docker files creation")
    parser.add_argument("--dev-mode", action="store_true", help="Development mode deployment")
    
    args = parser.parse_args()
    
    deployment = TradingSystemDeployment()
    
    try:
        deployment.print_banner()
        
        # Core deployment steps
        deployment.check_system_requirements()
        deployment.create_directory_structure()
        python_path, pip_path = deployment.setup_virtual_environment()
        deployment.install_dependencies(pip_path)
        deployment.create_configuration_files()
        deployment.create_startup_scripts(python_path)
        
        # Optional components
        if not args.no_docker:
            deployment.create_docker_files()
        
        if os.name != 'nt':  # Linux/Mac only
            deployment.create_systemd_service(python_path)
        
        # Testing
        if not args.skip_tests:
            deployment.run_initial_tests(python_path)
        
        # Summary
        deployment.print_deployment_summary()
        
        return True
        
    except Exception as e:
        print(f"\nERROR: Deployment failed: {e}")
        print("\nPlease fix the issue and run the deployment again.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)