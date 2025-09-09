# [STATE] Immunization Automation

An automated Python script that:
1. Extracts active student roster data from the school district's database
2. Formats it according to state immunization registry requirements
3. Emails the data to DOH staff who upload it to the state immunization tracking system
4. Enables the DOH to match student records with their immunization histories for compliance monitoring
## 🎯 Purpose

This application automates the tedious manual process of:
1. **Querying the database** for active student roster data
2. **Generating Excel reports** with immunization compliance information  
3. **Emailing reports** to designated staff members for processing
4. **Automatically handling school year transitions** every September 1st

## ✨ Key Features

### 🗓️ Automatic School Year Management
The system's **most important feature** is its automatic school year detection:

- **No manual updates required** - The script automatically calculates the correct school year based on the system date
- **September 1st transitions** - Seamlessly switches to the new school year without intervention
- **Smart date logic**: 
  - Before Sept 1st: Uses previous year (e.g., August 2025 = 2024 school year)
  - On/After Sept 1st: Uses current year (e.g., September 2025 = 2025 school year)

**Example Timeline:**
```
August 31, 2025    → School Year 2024 (2024-2025 academic year)
September 1, 2025  → School Year 2025 (2025-2026 academic year) 
September 1, 2026  → School Year 2026 (2026-2027 academic year)
```

### 🔒 Secure Configuration
- **Credentials protected** via gitignored `init.py` files
- **Database connections** using SQLAlchemy with connection pooling
- **No hardcoded passwords** or sensitive information in committed code

### 📧 Automated Email Distribution  
- **Excel attachments** generated automatically from query results
- **Multiple recipients** supported via configuration
- **Professional email templates** with report details and instructions
- **Portal links** included for easy data processing

### 🔄 Robust Error Handling
- **Database retry logic** for connection failures
- **Comprehensive logging** with rotating log files  
- **Email delivery confirmation** and failure notifications
- **Validation checks** for all critical components

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- Access to database
- Internal SMTP server access

### Installation

1. **Clone and setup environment:**
```bash
git clone <repository-url>
cd Immunization-Automation
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

2. **Configure credentials:**
```bash
cp src/config/init_example.py src/config/init.py
# Edit src/config/init.py with your actual credentials
```

3. **Test the setup:**
```bash
# Test database and email connections
python src/main.py --test-db --test-email

# Test full process without sending email
python src/main.py --dry-run
```

4. **Run the automation:**
```bash
python src/main.py
```

## 🛠️ Windows Task Scheduler Setup

For automated execution, use the included batch file:

1. **Configure Task Scheduler:**
   - Program/script: `C:\path\to\Immunization-Automation\run_automation.bat`
   - Start in: `C:\path\to\Immunization-Automation`
   - Run with highest privileges: Yes

2. **Schedule frequency:** Set based on your immunization reporting needs

## 📊 How the School Year Logic Works

### The Problem This Solves
Previously, the SQL query had a hardcoded year value:
```sql
AND yr.SCHOOL_YEAR = 2025  -- Had to manually update each September!
```

### The Automated Solution
The system now automatically:

1. **Reads the current date** from the system calendar
2. **Calculates the school year** using the September 1st transition rule
3. **Parameterizes the SQL query** to use the calculated year:
```sql
AND yr.SCHOOL_YEAR = :school_year  -- Automatically populated!
```

### School Year Calculation Logic
```python
def get_current_school_year():
    today = datetime.now()
    current_year = today.year
    
    # September 1st is the school year boundary
    school_year_start = datetime(current_year, 9, 1)  # Sept 1st
    
    if today < school_year_start:
        return current_year - 1  # Still in previous school year
    else:
        return current_year      # New school year has begun
```

### Real-World Examples
- **August 31, 2025 at 11:59 PM** → Returns `2024` (still in 2024-2025 school year)
- **September 1, 2025 at 12:01 AM** → Returns `2025` (new 2025-2026 school year)
- **December 15, 2025** → Returns `2025` (continuing 2025-2026 school year)
- **June 30, 2026** → Returns `2025` (still in 2025-2026 school year)
- **September 1, 2026** → Returns `2026` (new 2026-2027 school year begins)

## 📁 Project Structure

```
├── run_automation.bat       # Windows Task Scheduler execution file
├── requirements.txt         # Python dependencies
├── immunization_query.sql         # SQL query template (auto-parameterized)
├── src/
│   ├── main.py             # Main automation script
│   ├── config/
│   │   ├── init.py         # Actual credentials (GITIGNORED)
│   │   ├── init_example.py # Credential template
│   │   └── config.py       # Configuration management
│   ├── database/
│   │   ├── connection.py   # SQLAlchemy database manager
│   │   └── queries.py      # SQL query loader with parameterization
│   ├── email_service/
│   │   └── sender.py       # Email service with Excel attachments
│   └── utils/
│       ├── logging_setup.py # Logging configuration
│       └── school_year.py   # School year calculation logic
└── logs/                   # Application logs
```

## 🔧 Command Line Options

```bash
# Test database connectivity
python src/main.py --test-db

# Test email connectivity  
python src/main.py --test-email

# Test both connections
python src/main.py --test-db --test-email

# Run with specific school year (for testing)
python src/main.py --school-year 2026

# Generate report but don't send email
python src/main.py --dry-run

# Normal execution (automatic school year)
python src/main.py
```

## 📈 Benefits

### For IT Staff
- **Zero manual SQL updates** - No more remembering to change hardcoded years
- **Automated scheduling** - Set it and forget it with Windows Task Scheduler
- **Comprehensive logging** - Easy troubleshooting and monitoring
- **Secure credential management** - Credentials never committed to version control

### For School Administrative Staff  
- **Timely reports** - Automated delivery ensures no missed deadlines
- **Consistent format** - Standardized Excel reports every time
- **Direct links** - Email includes portal links for easy data processing
- **Multiple recipients** - Reports automatically distributed to all relevant staff

### For Compliance
- **Accurate school years** - Eliminates human error in year calculations
- **Audit trail** - Comprehensive logging of all operations
- **Data integrity** - Parameterized queries prevent SQL injection
- **Reliable delivery** - Email confirmation and retry logic

## 🛡️ Security Features

- **Credential isolation** - Database and email credentials stored in gitignored files
- **Parameterized queries** - Prevents SQL injection attacks  
- **Connection pooling** - Efficient and secure database connections
- **TLS support** - Encrypted email transmission when required
- **No hardcoded secrets** - All sensitive data externalized

## 🔄 Maintenance

### Automated (No Action Required)
- ✅ School year transitions every September 1st
- ✅ SQL query parameterization  
- ✅ Log file rotation
- ✅ Database connection management

### Manual Tasks
- Update email recipient lists as staff changes
- Monitor logs for any connectivity issues
- Test connections if infrastructure changes
- Update database credentials if they rotate

## 🚨 Troubleshooting

### Common Issues

**Email not sending:**
- Check SMTP server settings in `init.py`
- Verify `SMTP_USE_AUTH = False` for internal servers
- Test with: `python src/main.py --test-email`

**Database connection failed:**
- Verify database credentials in `init.py`
- Check network connectivity to database server
- Test with: `python src/main.py --test-db`

**Wrong school year:**
- Verify system date is correct
- Test calculation: `python src/main.py --dry-run`
- Override for testing: `python src/main.py --school-year 2025 --dry-run`

## 📞 Support

For technical issues or questions about this automation:
1. Check the logs in the `logs/` directory
2. Run diagnostic tests using the `--test-db` and `--test-email` flags
3. Consult the `CLAUDE.md` file for detailed technical documentation

---

**🎓 The bottom line:** This script eliminates the annual headache of manually updating SQL queries and ensures your immunization reporting stays current automatically, every September 1st!