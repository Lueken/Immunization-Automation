from config.init import *
import os
from pathlib import Path

# Database configuration
DATABASE_URL = f"mssql+pymssql://{DB_USERNAME}:{DB_PASSWORD}@{DB_SERVER}/{DB_DATABASE}"

# Email configuration
EMAIL_CONFIG = {
    'smtp_server': SMTP_SERVER,
    'smtp_port': SMTP_PORT,
    'use_tls': SMTP_USE_TLS,
    'use_auth': SMTP_USE_AUTH,
    'username': EMAIL_USERNAME,
    'password': EMAIL_PASSWORD,
    'from_email': FROM_EMAIL,
    'recipients': EMAIL_RECIPIENTS
}

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
SQL_QUERIES_PATH = PROJECT_ROOT / "immunization_query.sql"
LOGS_PATH = PROJECT_ROOT / "logs"

# Ensure logs directory exists
LOGS_PATH.mkdir(exist_ok=True)

# Logging configuration
LOG_CONFIG = {
    'filename': LOGS_PATH / 'immunization_automation.log',
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'max_bytes': 10 * 1024 * 1024,  # 10MB
    'backup_count': 5
}

# School year configuration
SCHOOL_YEAR_START_MONTH = 9  # September
SCHOOL_YEAR_START_DAY = 1    # 1st