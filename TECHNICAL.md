# TECHNICAL.md

## Project Overview

Immunization Automation - A Python script that automates the process of:
1. Running SQL queries against the Student Information System database
2. Extracting immunization data for the current school year
3. Emailing the results to staff members who handle immunization uploads

## Development Environment

- **Python Version**: 3.13.3
- **Virtual Environment**: Located in `.venv/` directory
- **IDE Configuration**: IntelliJ IDEA/PyCharm project files in `.idea/`

## Project Architecture

The automation system should include these key components:

### Core Modules
- **Database Connection**: SQLAlchemy with SQL Server connectivity
- **Query Execution**: SQL query runner with parameterized school year
- **Email Service**: SMTP email sender with attachment support
- **Configuration Management**: init.py file feeding config.py for secure credential handling
- **Scheduling Logic**: Automatic school year detection (updates September 1st)
- **Logging**: Comprehensive logging for monitoring and troubleshooting

### Configuration Requirements
- `init.py` file containing actual credentials (MUST be in .gitignore)
- `config.py` file that imports from init.py for database and email settings
- Email recipient lists
- SMTP server configuration
- School year calculation logic
- Query templates with year parameters

## Common Commands

```bash
# Activate virtual environment (Windows)
.venv\Scripts\activate

# Install dependencies from requirements.txt
pip install -r requirements.txt

# Or install core dependencies manually
pip install sqlalchemy pymssql pandas openpyxl schedule python-dotenv

# Alternative SQL Server driver if pymssql has issues
pip install sqlalchemy pyodbc pandas openpyxl schedule python-dotenv

# Run the main automation script
python main.py

# Run with specific school year override
python main.py --school-year 2025

# Test email functionality
python test_email.py

# Generate requirements file
pip freeze > requirements.txt

# Execute via Windows Task Scheduler
run_automation.bat
```

## Windows Task Scheduler Integration

The project includes a `run_automation.bat` file for Windows Task Scheduler execution:

```batch
@echo off
cd /d "C:\path\to\Immunization-Automation"
call .venv\Scripts\activate
python src\main.py
pause
```

### Task Scheduler Setup
- **Program/script**: Full path to `run_automation.bat`
- **Start in**: Project root directory
- **Run with highest privileges**: Yes (if database access requires it)
- **Schedule**: Configure based on immunization reporting needs

## Security Configuration Pattern

### File Structure for Credentials
```
config/
├── init.py          # Contains actual credentials (NEVER commit - must be in .gitignore)
├── config.py        # Imports from init.py, handles configuration logic
└── init_example.py  # Template showing required variables (safe to commit)
```

### init.py (in .gitignore)
```python
# Database credentials
DB_SERVER = "your-server.domain.com"
DB_DATABASE = "IMMUNIZATION_DB"
DB_USERNAME = "your_username"
DB_PASSWORD = "your_password"

# Email credentials
SMTP_SERVER = "smtp.yourdomain.com"
SMTP_PORT = 587
EMAIL_USERNAME = "automation@yourdomain.com"
EMAIL_PASSWORD = "your_email_password"
```

### config.py (safe to commit)
```python
from config.init import *
import sqlalchemy

# Build connection string from init.py credentials
DATABASE_URL = f"mssql+pymssql://{DB_USERNAME}:{DB_PASSWORD}@{DB_SERVER}/{DB_DATABASE}"

# Email configuration
EMAIL_CONFIG = {
    'smtp_server': SMTP_SERVER,
    'smtp_port': SMTP_PORT,
    'username': EMAIL_USERNAME,
    'password': EMAIL_PASSWORD
}
```

## Key Implementation Considerations

### Database Connection (SQLAlchemy)
- Use SQLAlchemy with pymssql driver for SQL Server (preferred over pyodbc due to environment issues)
- Connection managed through config.py which imports from init.py
- Implement connection pooling and retry logic
- Use parameterized queries to prevent SQL injection

### School Year Logic (Critical Feature)
The system automatically calculates and updates the school year without manual intervention:

**Automatic School Year Detection:**
- School years run from September 1st to August 31st
- **Before September 1st**: Uses previous calendar year (e.g., August 2025 = 2024 school year)
- **On/After September 1st**: Uses current calendar year (e.g., September 2025 = 2025 school year)

**SQL Query Parameterization:**
- Original hardcoded: `AND yr.SCHOOL_YEAR = 2025`
- Automatically converted to: `AND yr.SCHOOL_YEAR = :school_year`
- Parameter value calculated from system date using `get_current_school_year()`

**Examples:**
- **2025-08-31**: Returns school year `2024` (still in 2024-2025 school year)
- **2025-09-01**: Returns school year `2025` (new 2025-2026 school year begins)
- **2026-09-01**: Returns school year `2026` (automatically transitions)

**No Manual Updates Required:** The script eliminates the need to manually update SQL queries each September.

### Security Best Practices
- `init.py` file MUST be in .gitignore to protect credentials
- Provide `init_example.py` template for setup guidance
- Never commit actual database credentials or email passwords
- Use SQLAlchemy connection pooling for database efficiency
- Implement retry logic for network operations

### Error Handling
- Database connection failures
- Missing init.py file
- Query execution errors
- Email delivery failures
- File attachment issues
- Network timeouts

## Typical Project Structure

```
├── run_automation.bat   # Windows Task Scheduler execution file
├── src/
│   ├── main.py              # Main automation script
│   ├── database/
│   │   ├── connection.py    # SQLAlchemy connection management
│   │   └── queries.py       # SQL query definitions
│   ├── email_service/
│   │   ├── sender.py        # Email functionality
│   │   └── templates.py     # Email templates
│   ├── utils/
│   │   ├── logging.py       # Logging setup
│   │   └── scheduler.py     # Year calculation and scheduling
│   ├── config/
│   │   ├── init.py          # Actual credentials (GITIGNORED)
│   │   ├── init_example.py  # Credential template
│   │   ├── config.py        # Configuration management
│   │   └── recipients.json  # Email recipient configuration
│   └── tests/
├── logs/                    # Log files directory
└── .gitignore              # MUST include config/init.py
```

## Required .gitignore entries
```
# Credential files
config/init.py

# Virtual environment
.venv/

# IDE files
.idea/
```

## Dependencies

All dependencies are listed in `requirements.txt`. Key packages include:
- `sqlalchemy>=1.4.0,<2.0.0` - Database ORM and connectivity (1.4.x for Python 3.13 compatibility)
- `pymssql>=2.2.0` - SQL Server driver for SQLAlchemy
- `pandas>=2.0.0` - Data manipulation
- `openpyxl>=3.1.0` - Excel file generation
- `schedule>=1.2.0` - Task scheduling
- `python-dotenv>=1.0.0` - Environment variable management

Built-in Python modules also used:
- `logging` - Application logging
- `smtplib` - Email sending
- `datetime` - Date/time operations

## Setup Instructions for New Environments
1. Install dependencies: `pip install -r requirements.txt`
2. Copy `src/config/init_example.py` to `src/config/init.py`
3. Fill in actual credentials in `src/config/init.py`
4. Verify `src/config/init.py` is listed in `.gitignore`
5. Test connections: `python src/main.py --test-db --test-email`
6. Test the full process: `python src/main.py --dry-run`

## Annual Maintenance

**September 1st Transition (Automated):**
- ✅ School year calculation updates automatically
- ✅ SQL queries use new school year parameter automatically
- ✅ No manual SQL query updates required

**Manual Tasks:**
- Update recipient lists in `src/config/init.py` as staff changes
- Test database connectivity and credentials if systems change
- Review and update SQL queries only if database schema changes
- Verify logs around September 1st to ensure smooth transition

**Testing School Year Logic:**
```bash
# Test with specific school year override
python src/main.py --school-year 2026 --dry-run

# Test current automatic detection
python src/main.py --dry-run
```