import logging
from pathlib import Path
from config.config import SQL_QUERIES_PATH
from utils.school_year import get_current_school_year

logger = logging.getLogger('waiis_automation.queries')

class QueryManager:
    def __init__(self):
        self.sql_file_path = SQL_QUERIES_PATH
    
    def load_waiis_query(self, school_year=None):
        """
        Load and parameterize the WAIIS query from the SQL file.
        
        Args:
            school_year (int, optional): School year to use. If None, uses current school year.
            
        Returns:
            str: Parameterized SQL query
        """
        if school_year is None:
            school_year = get_current_school_year()
        
        logger.info(f"Loading WAIIS query for school year {school_year}")
        
        try:
            with open(self.sql_file_path, 'r', encoding='utf-8') as file:
                query_template = file.read()
            
            # SQL file already contains :school_year parameter
            logger.info("WAIIS query loaded successfully")
            return query_template
            
        except FileNotFoundError:
            logger.error(f"SQL query file not found: {self.sql_file_path}")
            raise
        except Exception as e:
            logger.error(f"Error loading SQL query: {e}")
            raise
    
    def get_query_parameters(self, school_year=None):
        """
        Get the parameters dictionary for the WAIIS query.
        
        Args:
            school_year (int, optional): School year to use. If None, uses current school year.
            
        Returns:
            dict: Parameters for the SQL query
        """
        if school_year is None:
            school_year = get_current_school_year()
        
        return {
            'school_year': school_year
        }
    
    def validate_query_file(self):
        """
        Validate that the SQL query file exists and is readable.
        
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            if not self.sql_file_path.exists():
                logger.error(f"SQL query file does not exist: {self.sql_file_path}")
                return False
            
            if not self.sql_file_path.is_file():
                logger.error(f"SQL query path is not a file: {self.sql_file_path}")
                return False
            
            # Try to read the file
            with open(self.sql_file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                if not content.strip():
                    logger.error("SQL query file is empty")
                    return False
            
            logger.info("SQL query file validation successful")
            return True
            
        except Exception as e:
            logger.error(f"Error validating SQL query file: {e}")
            return False