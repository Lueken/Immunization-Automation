from datetime import datetime
from config.config import SCHOOL_YEAR_START_MONTH, SCHOOL_YEAR_START_DAY

def get_current_school_year():
    """
    Calculate the current school year based on today's date.
    School year starts September 1st and ends August 31st.
    
    Returns:
        int: The current school year (e.g., 2024 for 2024-2025 school year)
    """
    today = datetime.now()
    current_year = today.year
    
    # If we're before September 1st, we're still in the previous school year
    school_year_start = datetime(current_year, SCHOOL_YEAR_START_MONTH, SCHOOL_YEAR_START_DAY)
    
    if today < school_year_start:
        return current_year - 1
    else:
        return current_year

def get_school_year_string(year=None):
    """
    Get formatted school year string.
    
    Args:
        year (int, optional): School year. If None, uses current school year.
        
    Returns:
        str: Formatted school year string (e.g., "2024-2025")
    """
    if year is None:
        year = get_current_school_year()
    
    return f"{year}-{year + 1}"

def validate_school_year(year):
    """
    Validate that a school year is reasonable.
    
    Args:
        year (int): School year to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    current_year = datetime.now().year
    # Allow school years from 10 years ago to 5 years in the future
    return (current_year - 10) <= year <= (current_year + 5)