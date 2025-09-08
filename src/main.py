#!/usr/bin/env python3
"""
WAIIS Immunization Automation Script

This script automates the process of:
1. Running SQL queries against the WAIIS database
2. Extracting immunization data for the current school year
3. Emailing the results to staff members

Usage:
    python main.py [--school-year YYYY] [--test-email] [--test-db]
"""

import argparse
import sys
import logging
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from utils.logging_setup import setup_logging
from utils.school_year import get_current_school_year, validate_school_year, get_school_year_string
from database.connection import DatabaseManager
from database.queries import QueryManager
from email_service.sender import EmailSender

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='WAIIS Immunization Automation')
    parser.add_argument(
        '--school-year', 
        type=int, 
        help='Override school year (default: current school year)'
    )
    parser.add_argument(
        '--test-email', 
        action='store_true', 
        help='Test email connection without sending report'
    )
    parser.add_argument(
        '--test-db', 
        action='store_true', 
        help='Test database connection without running query'
    )
    parser.add_argument(
        '--dry-run', 
        action='store_true', 
        help='Run query but do not send email'
    )
    
    return parser.parse_args()

def test_database_connection(db_manager):
    """Test database connectivity."""
    logger = logging.getLogger('waiis_automation.main')
    logger.info("Testing database connection...")
    
    if db_manager.test_connection():
        logger.info("Database connection test: PASSED")
        return True
    else:
        logger.error("Database connection test: FAILED")
        return False

def test_email_connection(email_sender):
    """Test email connectivity."""
    logger = logging.getLogger('waiis_automation.main')
    logger.info("Testing email connection...")
    
    if email_sender.test_email_connection():
        logger.info("Email connection test: PASSED")
        return True
    else:
        logger.error("Email connection test: FAILED")
        return False

def run_immunization_report(school_year=None, dry_run=False):
    """
    Run the complete immunization report process.
    
    Args:
        school_year (int, optional): School year to process
        dry_run (bool): If True, run query but don't send email
        
    Returns:
        bool: True if successful, False otherwise
    """
    logger = logging.getLogger('waiis_automation.main')
    
    try:
        # Initialize components
        db_manager = DatabaseManager()
        query_manager = QueryManager()
        email_sender = EmailSender()
        
        # Determine school year
        if school_year is None:
            school_year = get_current_school_year()
        
        if not validate_school_year(school_year):
            logger.error(f"Invalid school year: {school_year}")
            return False
        
        logger.info(f"Processing immunization report for school year {get_school_year_string(school_year)}")
        
        # Validate query file
        if not query_manager.validate_query_file():
            logger.error("Query file validation failed")
            return False
        
        # Test database connection
        if not test_database_connection(db_manager):
            return False
        
        # Load and execute query
        logger.info("Loading and executing WAIIS query...")
        query = query_manager.load_waiis_query(school_year)
        parameters = query_manager.get_query_parameters(school_year)
        
        data = db_manager.execute_query(query, parameters)
        logger.info(f"Query executed successfully, retrieved {len(data)} records")
        
        if not data:
            logger.warning("No data returned from query - this may indicate an issue")
        
        # Send email (unless dry run)
        if dry_run:
            logger.info("Dry run mode: Skipping email sending")
            logger.info(f"Would have sent report with {len(data)} records")
        else:
            logger.info("Sending immunization report email...")
            if email_sender.send_email(data, school_year):
                logger.info("Immunization report sent successfully")
            else:
                logger.error("Failed to send immunization report")
                return False
        
        return True
        
    except Exception as e:
        logger.error(f"Error in immunization report process: {e}", exc_info=True)
        return False
    finally:
        # Clean up database connections
        if 'db_manager' in locals():
            db_manager.close()

def main():
    """Main entry point."""
    # Setup logging
    logger = setup_logging()
    logger.info("Starting WAIIS Immunization Automation")
    
    try:
        # Parse arguments
        args = parse_arguments()
        
        # Validate school year if provided
        if args.school_year and not validate_school_year(args.school_year):
            logger.error(f"Invalid school year: {args.school_year}")
            return 1
        
        # Handle test modes
        if args.test_db or args.test_email:
            overall_success = True
            
            if args.test_db:
                db_manager = DatabaseManager()
                db_success = test_database_connection(db_manager)
                db_manager.close()
                overall_success = overall_success and db_success
            
            if args.test_email:
                email_sender = EmailSender()
                email_success = test_email_connection(email_sender)
                overall_success = overall_success and email_success
            
            return 0 if overall_success else 1
        
        # Run the main process
        success = run_immunization_report(
            school_year=args.school_year,
            dry_run=args.dry_run
        )
        
        if success:
            logger.info("WAIIS Immunization Automation completed successfully")
            return 0
        else:
            logger.error("WAIIS Immunization Automation failed")
            return 1
            
    except KeyboardInterrupt:
        logger.info("Process interrupted by user")
        return 130
    except Exception as e:
        logger.error(f"Unexpected error in main process: {e}", exc_info=True)
        return 1

if __name__ == "__main__":
    sys.exit(main())