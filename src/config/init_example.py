# Database credentials - Copy this file to init.py and fill in actual values
DB_SERVER = "your-sql-server.domain.com"
DB_DATABASE = "your_database_name"
DB_USERNAME = "your_username"
DB_PASSWORD = "your_password"

# Email credentials
SMTP_SERVER = "smtp.yourdomain.com"
SMTP_PORT = 25  # Use 25 for internal SMTP, 587 for external with TLS
SMTP_USE_TLS = False  # Set to False for port 25 internal SMTP, True for port 587
SMTP_USE_AUTH = False  # Set to False for internal SMTP that doesn't require authentication
EMAIL_USERNAME = "your_email@yourdomain.com"  # Not used if SMTP_USE_AUTH = False
EMAIL_PASSWORD = "your_email_password"       # Not used if SMTP_USE_AUTH = False
FROM_EMAIL = "your_email@yourdomain.com"

# Email recipients for immunization reports
EMAIL_RECIPIENTS = [
    "recipient1@yourdomain.com",
    "recipient2@yourdomain.com"
    # Add more recipients as needed
]