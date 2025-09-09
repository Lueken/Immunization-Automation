import logging
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from config.config import DATABASE_URL
import time

logger = logging.getLogger('immunization_automation.database')

class DatabaseManager:
    def __init__(self, max_retries=3, retry_delay=5):
        self.engine = None
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self._initialize_engine()
    
    def _initialize_engine(self):
        """Initialize the database engine with connection pooling."""
        try:
            self.engine = create_engine(
                DATABASE_URL,
                pool_pre_ping=True,  # Verify connections before use
                pool_recycle=3600,   # Recycle connections after 1 hour
                echo=False           # Set to True for SQL debugging
            )
            logger.info("Database engine initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize database engine: {e}")
            raise
    
    def test_connection(self):
        """Test database connectivity."""
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text("SELECT 1"))
                return result.fetchone()[0] == 1
        except Exception as e:
            logger.error(f"Database connection test failed: {e}")
            return False
    
    def execute_query(self, query, parameters=None):
        """
        Execute a SQL query with retry logic.
        
        Args:
            query (str): SQL query to execute
            parameters (dict, optional): Query parameters
            
        Returns:
            list: Query results as list of dictionaries
        """
        for attempt in range(self.max_retries):
            try:
                with self.engine.connect() as connection:
                    if parameters:
                        result = connection.execute(text(query), parameters)
                    else:
                        result = connection.execute(text(query))
                    
                    # Convert result to list of dictionaries
                    columns = result.keys()
                    rows = result.fetchall()
                    return [dict(zip(columns, row)) for row in rows]
                    
            except SQLAlchemyError as e:
                logger.warning(f"Database query attempt {attempt + 1} failed: {e}")
                if attempt < self.max_retries - 1:
                    logger.info(f"Retrying in {self.retry_delay} seconds...")
                    time.sleep(self.retry_delay)
                else:
                    logger.error(f"All {self.max_retries} database query attempts failed")
                    raise
            except Exception as e:
                logger.error(f"Unexpected error during database query: {e}")
                raise
    
    def close(self):
        """Close database connections."""
        if self.engine:
            self.engine.dispose()
            logger.info("Database connections closed")