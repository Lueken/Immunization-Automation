import logging
import smtplib
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from io import BytesIO, StringIO
from datetime import datetime
from config.config import EMAIL_CONFIG
from utils.school_year import get_school_year_string

logger = logging.getLogger('immunization_automation.email')

class EmailSender:
    def __init__(self):
        self.config = EMAIL_CONFIG

    def create_csv_attachment(self, data, filename=None):
        """
        Create CSV file from query results.

        Args:
            data (list): Query results as list of dictionaries
            filename (str, optional): Filename for the attachment

        Returns:
            BytesIO: CSV file as bytes
        """
        if not data:
            logger.warning("No data provided for CSV attachment")
            return None

        try:
            # Convert to DataFrame
            df = pd.DataFrame(data)

            # Create CSV file in memory
            csv_buffer = StringIO()
            df.to_csv(csv_buffer, index=False, encoding='utf-8')

            # Convert StringIO to BytesIO for attachment
            csv_bytes = BytesIO(csv_buffer.getvalue().encode('utf-8'))
            csv_bytes.seek(0)

            logger.info(f"CSV attachment created with {len(data)} records")
            return csv_bytes

        except Exception as e:
            logger.error(f"Error creating CSV attachment: {e}")
            raise

    def create_email_message(self, data, school_year=None):
        """
        Create the email message with attachment.

        Args:
            data (list): Query results as list of dictionaries
            school_year (int, optional): School year for the report

        Returns:
            MIMEMultipart: Email message object
        """
        if school_year is None:
            from utils.school_year import get_current_school_year
            school_year = get_current_school_year()

        school_year_str = get_school_year_string(school_year)

        # Create message
        msg = MIMEMultipart()
        msg['From'] = self.config['from_email']
        msg['To'] = ", ".join(self.config['recipients'])
        msg['Subject'] = f"Immunization Report - {school_year_str}"

        # Email body
        body = f"""
Dear Staff,

Please find attached the Immunization Report for school year {school_year_str}.

Report Details:
- Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- Records: {len(data) if data else 0}
- School Year: {school_year_str}
- Format: CSV (Comma-Separated Values)

This report contains active student roster data for immunization tracking, excluding students without an SSID and students enrolled in program 696.

The CSV file can be opened in Excel, Google Sheets, or any spreadsheet application for processing.

Please process this data according to our immunization compliance procedures via the Immunization Portal.

https://your-immunization-portal.gov/surveys/

Best regards,
Immunization Automation System
        """.strip()

        msg.attach(MIMEText(body, 'plain'))

        # Create and attach CSV file
        if data:
            csv_buffer = self.create_csv_attachment(data)
            if csv_buffer:
                attachment = MIMEBase('application', 'csv')
                attachment.set_payload(csv_buffer.read())
                encoders.encode_base64(attachment)

                filename = f"Immunization_Report_{school_year_str}_{datetime.now().strftime('%Y%m%d')}.csv"
                attachment.add_header(
                    'Content-Disposition',
                    f'attachment; filename= {filename}'
                )
                msg.attach(attachment)
                logger.info(f"CSV attachment added: {filename}")

        return msg

    def send_email(self, data, school_year=None):
        """
        Send the immunization report email.
        
        Args:
            data (list): Query results as list of dictionaries
            school_year (int, optional): School year for the report
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            logger.info("Preparing to send immunization report email")

            # Create email message
            msg = self.create_email_message(data, school_year)

            # Connect to SMTP server and send email
            with smtplib.SMTP(self.config['smtp_server'], self.config['smtp_port']) as server:
                if self.config.get('use_tls', True):
                    server.starttls()

                # Only authenticate if required
                if self.config.get('use_auth', True):
                    server.login(self.config['username'], self.config['password'])

                text = msg.as_string()
                server.sendmail(
                    self.config['from_email'],
                    self.config['recipients'],
                    text
                )

            logger.info(f"Email sent successfully to {len(self.config['recipients'])} recipients")
            return True

        except smtplib.SMTPException as e:
            logger.error(f"SMTP error sending email: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error sending email: {e}")
            return False

    def test_email_connection(self):
        """
        Test SMTP connection without sending an email.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            with smtplib.SMTP(self.config['smtp_server'], self.config['smtp_port']) as server:
                if self.config.get('use_tls', True):
                    server.starttls()

                # Only authenticate if required
                if self.config.get('use_auth', True):
                    server.login(self.config['username'], self.config['password'])

            logger.info("Email connection test successful")
            return True

        except Exception as e:
            logger.error(f"Email connection test failed: {e}")
            return False