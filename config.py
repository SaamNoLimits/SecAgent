"""
Configuration file for SecAgent - Red Team Pentesting Assistant
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # LLM API Keys
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
    
    # Default LLM Model
    DEFAULT_MODEL = "gpt-4"
    ANTHROPIC_MODEL = "claude-3-sonnet-20240229"
    
    # Security APIs
    SHODAN_API_KEY = os.getenv('SHODAN_API_KEY')
    CENSYS_API_ID = os.getenv('CENSYS_API_ID')
    CENSYS_API_SECRET = os.getenv('CENSYS_API_SECRET')
    
    # Output Settings
    OUTPUT_DIR = "output"
    REPORTS_DIR = "reports"
    LOGS_DIR = "logs"
    
    # Scanning Settings
    DEFAULT_TIMEOUT = 30
    MAX_THREADS = 50
    
    # Web Settings
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    ]
    
    # Wordlists
    COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 993, 995, 1723, 3306, 3389, 5900, 8080]
    COMMON_SUBDOMAINS = ["www", "mail", "ftp", "admin", "test", "dev", "staging", "api", "blog", "shop"]
